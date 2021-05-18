import json
from typing import NewType, List, Tuple, Union
from dataclasses import dataclass, field, asdict


"""
Manual type partial hierarchy:
Google\ Drive/ASKE-AutoMATES/ASKE-E/GroMEt-model-representation-WG/figs/
    GrometElm-hierarchy.graffle
    gromet_uml_2021-05-16.{svg,png}

/ASKE-AutoMATES/ASKE-E/GroMEt-model-representation-WG/gromet-examples
    gromet-examples.graffle
        Conditional
        Loop
        toy1 examples
        ...

TODO: Side Effects
() mutations of globals
    (can happen in libraries)
() mutations of mutable variables
() mutations of referenced variables (C/C++, can't occur in Python)

Event-driven programming
() No static trace (directed edges from one fn to another), 
    so a generalization of side-effects
    Requires undirected, which corresponds to under-specification 


GroMEt is the bytecode for the expression of multi-framework model types

The GroMEt bytecode is expressed in a syntax of building-blocks
  The gromet type specifies the semantic interpretation to be used for
    for the syntactic types.

Directed GroMET is the bytecode for causal/influence paths / data flow semantics

Functions are Directed Boxes that represent directed paths in the general
  case of a (directed) graph
Expression Boxes represent a special kind of Box whose internal 'wiring' are
  guaranteed to be (must be) a tree, where any references to variables
  (value sources) are via the input ports to the Expression.
  The internal wiring is thus a recursive list of input ports and Exp
     where Exp is an expression consisting of a single operator (primitive
     or Box name) and arguments (positionally presented) to the operator
  An Expression has a single output port that passes the result of the top Exp
"""

# -----------------------------------------------------------------------------
# GroMEt syntactic types
# -----------------------------------------------------------------------------

# The following gromet spec as a "grammar" is not guaranteed to
#   be unambiguous.
# For this reason, adding explicit "gromet_element" field that
#   represents the Type of GroMEt syntactic element


@dataclass
class GrometElm(object):
    """
    Base class for all Gromet Elements.
    Implements __post_init__ that saves syntactic type (syntax) as GroMEt element class name.
    """
    syntax: str = field(init=False)

    def __post_init__(self):
        self.syntax = self.__class__.__name__


# --------------------
# Uid

# The purpose here is to provide a kind of "namespace" for the unique IDs
# that used to distinguish gromet model component instances.
# Currently making these str so I can give them arbitrary names as I
#   hand-construct example GroMEt instances, but these could be
#   sequential integers (as James uses) or uuids.

UidMetadatum = NewType('UidMetadatum', str)
UidType = NewType('UidType', str)
UidLiteral = NewType('UidLiteral', str)
UidPort = NewType('UidPort', str)
UidJunction = NewType('UidJunction', str)
UidWire = NewType('UidWire', str)

UidBox = NewType('UidBox', str)

UidOp = NewType('UidOp', str)  # Primitive operator name
UidFn = NewType('UidFn', str)  # Defined function name

UidVariable = NewType('UidVariable', str)
UidGromet = NewType('UidGromet', str)


# Explicit "reference" objects.
# Required when there is ambiguity about which type of uid reference
# is specified.

@dataclass
class RefFn(GrometElm):
    """
    Representation of an explicit reference to a defined box
    """
    name: UidFn


@dataclass
class RefOp(GrometElm):
    """
    Representation of an explicit reference to a primitive operator
    """
    name: UidOp


# --------------------
# TypedGrometElm

@dataclass
class TypedGrometElm(GrometElm):
    """
    Base class for all Gromet Elements that may be typed.
    """
    type: Union[UidType, None]


# --------------------
# Metadata

@dataclass
class Metadatum(TypedGrometElm):
    """
    Metadatum base.
    """
    uid: UidMetadatum


# TODO: add Metadatum subtypes
#       Will be based on: https://ml4ai.github.io/automates-v2/grfn_metadata.html


Metadata = NewType('Metadata', Union[List[Metadatum], None])


# --------------------
# Type


@dataclass
class Type:
    """
    Type Specification.
    Constructed as an expression of the GroMEt Type Algebra
    """
    type: str = field(init=False)

    def __post_init__(self):
        self.type = type(self).__name__


@dataclass
class TypeDeclaration(GrometElm):
    name: UidType
    type: Type
    metadata: Metadata

# TODO: GroMEt type algebra: "sublangauge" for specifying types


# Atomics

@dataclass
class Atomic(Type):
    pass


# @dataclass
# class Any(Atomic):
#     pass
#
#
# @dataclass
# class Nothing(Atomic):
#     pass
#
#
# @dataclass
# class Number(Atomic):
#     pass
#
#
# @dataclass
# class Integer(Number):
#     pass
#
#
# @dataclass
# class Real(Number):
#     pass
#
#
# @dataclass
# class Float(Real):
#     pass
#
#
# @dataclass
# class Boolean(Atomic):
#     pass
#
#
# @dataclass
# class Character(Atomic):
#     pass
#
#
# @dataclass
# class Symbol(Atomic):
#     pass


# Composites

@dataclass
class Composite(Type):
    pass


# Algebra

# @dataclass
# class Prod(Composite):
#     element_type: List[UidType]
#     cardinality: Union[int, None]
#
#
# @dataclass
# class String(Prod):
#     element_type: List[UidType]
#
#
# @dataclass
# class Sum(Composite):
#     element_type: List[UidType]
#
#
# @dataclass
# class NamedAttribute(Composite):
#     name: str
#     element_type: UidType
#
#
# @dataclass
# class Map(Prod):
#     element_type: List[Tuple[UidType, UidType]]


# --------------------
# Literal


@dataclass
class Literal(TypedGrometElm):
    """
    Literal base.
    A literal is an instances of Types
    """
    uid: Union[UidLiteral, None]  # allows anonymous literals
    value: 'Val'  # TODO
    metadata: Metadata


# TODO: "sublanguage" for specifying instances

@dataclass
class Val(GrometElm):
    val: Union[str, List[Union['Val', 'AttributeVal']]]


@dataclass
class AttributeVal(GrometElm):
    name: str
    val: Val


'''
Interval Number, Number, Number

Type: Pair = Prod(element_type[Int, String]) --> (<int>, <string>)
Literal: (type: "Pair", [3, "hello"])

Literal: (type: "Interval", [3, 6.7, 0.001])

SetIntegers = Prod(element_type=[Int])
SetIntegers10 = Prod(element_type=[Int], 10)
Literal: (type: "SetInt10", [1,2,3,3,4,52....])
'''


# --------------------
# Valued

@dataclass
class Valued(TypedGrometElm):
    """
    Typed Gromet Elements that have a value.
    These elements may also be named.
    """
    value: Union[Literal, None]
    name: Union[str, None]


# --------------------
# Junction

@dataclass
class Junction(Valued):
    """
    Junction base.
    Junctions are "0-ary"
    """
    uid: UidJunction
    metadata: Metadata


# --------------------
# Port

@dataclass
class Port(Valued):
    """
    Port base.
    Ports are "1-ary" as they always *must* belong to a single Box
        -- you cannot have a Port without a host Box.
    Ports define an interface to a Box, whereby values may pass from
        outside of the Box into the internals of the Box.
    A Port may be optionally named (e.g., named argument)
    """
    uid: UidPort
    box: UidBox
    metadata: Metadata


# --------------------
# Wire

@dataclass
class Wire(Valued):
    """
    Wire base. Not intended to be instantiated.
    Wires are "2-ary" as they connect up to two elements.
    All Wires have a Type (of the value they may carry).
    Optionally declared with a value, otherwise derived (from system dynamics).
    """
    uid: UidWire
    metadata: Metadata


@dataclass
class WireDirected(Wire):
    """
    Directed Wire base.
    Has optional single input and single output Port or Junction.
    Not enforced, but assume one WireDirected is NOT between two Junctions.
    """
    input: Union[UidPort, UidJunction, None]
    output: Union[UidPort, UidJunction,  None]


@dataclass
class WireUndirected(Wire):
    """
    Undirected Wire base.
    Undirected Wire connects two value-carrying endpoints: Port or Junction
    """
    end_points: Union[Tuple[Union[UidPort, UidJunction, None],
                            Union[UidPort, UidJunction, None]],
                      None]


# --------------------
# Box

@dataclass
class Box(TypedGrometElm):
    """
    Box base.
    A Box may have a name.
    A Box may have wiring (set of wiring connecting Ports of Boxes)
    """
    uid: UidBox
    name: Union[str, None]

    metadata: Metadata


@dataclass
class HasContents:
    """
    Box "contents" references
    NOTE:
        Natural to think of boxes "containing" (immediately
            contained) Boxes, Junctions and Wires that wire up
            the elements.
        This information functions like an index and
            supports easier identification of the elements
            that are the "top level contents" of a Box.
        Other Boxes do also have contents, but have special
            intended structure that is explicitly represented
    """
    wires: Union[List[UidWire], None]
    boxes: Union[List[UidBox], None]
    junctions: Union[List[UidJunction], None]


@dataclass
class BoxUndirected(Box):
    """
    Undirected Box base.
    Unoriented list of Ports represent interface to Box
    """

    # NOTE: Redundant since Ports specify the Box they belong to.
    # However, natural to think of boxes "having" Ports, and DirectedBoxes
    # must specify the "face" their ports belong to, so for parity we'll
    # have BoxUndirected also name their Ports
    ports: Union[List[UidPort], None]


@dataclass
class BoxDirected(Box):
    # NOTE: This is NOT redundant since Ports are not oriented,
    # but DirectedBox has ports on a "orientation/face"
    input_ports: Union[List[UidPort], None]
    output_ports: Union[List[UidPort], None]


# Relations

@dataclass
class Relation(BoxUndirected, HasContents):
    """
    Base Relation
    """
    pass


@dataclass
class PetriEvent(BoxUndirected):
    enabling_condition: Relation
    rate: Relation
    effect: Relation


# Functions

@dataclass
class Function(BoxDirected, HasContents):
    """
    Base Function
    Representations of general functions with contents wiring
        inputs to outputs.
    """
    pass


@dataclass
class Expr(GrometElm):
    """
    Assumption that may need revisiting:
      Expr's are assumed to always be declared inline as single instances,
      and may include Expr's in their args.
      Under this assumption, they do not require a uid or name
      -- they are always anonymous single instances.
    The call field of an Expr is a reference, either to
        (a) RefOp: primitive operator.
        (b) RefOp: an explicitly defined Box (e.g., a Function)
    The args field is a list of: UidPort reference, Literal or Expr
    """
    call: Union[RefFn, RefOp]
    args: Union[List[Union[UidPort, Literal, 'Expr']], None]


@dataclass
class Expression(BoxDirected):
    """
    A BoxDirected who's contents are an expression tree of Exp's.
    Assumptions:
      (1) Any "value" references in the tree will refer to the
        input Ports of the Expression. For this reason, there is
        no need for Wires.
      (2) An Expression always has only one output Port, but for
        parity with BoxDirected, the "output_ports" field name
        remains plural and is a List (of always one Port).
    """
    tree: Expr


@dataclass
class Predicate(Expression):
    """
    A Predicate is an Expression that has
        an assumed Boolean output Port
      (although we will not override the parent
       BoxDirected parent).
    """
    pass


@dataclass
class Conditional(BoxDirected):
    """
    Conditional
        ( TODO:
            Assumes no side effects.
            Assumes no breaks.
        )
    ( NOTE: the following notes make references to elements as they
            appear in Clay's gromet visual notation. )
    Terminology:
        *branch Predicate* (a type of Expression computing a
            boolean) represents the branch conditional test whose
            outcome determines whether the branch will be executed.
        *branch Function* represents the computation of anything in
            the branch
        A *branch* itself consists of a Tuple of:
                <Predicate>, <Function>, List[UidWire]
            The UidWire list denotes the set of wires relevant for
                completely wiring the branch Cond and Fn to the
                Conditional input and output Ports.
    Port conventions:
        Being a BoxDirected, a Conditional has a set of
            input and output Ports.
        *input* Ports capture any values of state/variables
            from the scope outside of the Conditional Box that
            are required by any branch Predicate or Function.
            (think of the input Ports as representing the relevant
            "variable environment" to the Conditional.)
        We can then think of each branch Function as a possible
            modification to the "variable environment" of the
            input Ports. When a branch Function is evaluated, it
            may preserve the values from some or all of the original
            input ports, or it may modify them, and/or it may
            introduce *new* variables resulting in corresponding
            new output Ports.
        From the perspective of the output Ports of the Conditional,
            we need to consider all of the possible new variable
            environment changes made by the selection of any branch.
            Doing so permits us to treat the Conditional as a modular
            building-block to other model structures.
            To achieve this, each branch Function must include in its
            output_ports a set of Ports that represent any of the
            "new variables" introduced by any branch Function.
            This allows us to have a single output_ports set for the
            entire Conditional, and whichever branch Function is
            evaluated, those Ports will be defined.
        NOTE: this does NOT mean those Ports are "Wired" and carry
            values; branch Function B1 may introduce a new variable
            "x" that branch Function B2 does not; B2 must still have
            a Port corresponding to "x", but it will not be Wired to
            anything -- it carries no value.
        Each branch Predicate has a single Boolean Port devoted to
            determining whether the branch is selected (when True).
    Definition: A Conditional is a...
        Sequence (List) of branches:
            Tuple[Predicate, Function, List[UidWire]]
        Each branch Predicate has a single boolean output Port
            whose state determines whether the branch Function
            will be evaluated to produce the state of the Conditional
            output Ports.
    Interpretation:
        GrFN provides unambiguous full data flow semantics.
        Here (for now), a gromet Conditional provides some abstraction
            away from pure data flow (but it is directly recoverable
            if desired).
        The interpretation convention:
            Branches are visited in order until the current branch
                Predicate evals to True
            If a branch Predicates evaluates to True, then branch
                Function takes the Conitional input_ports and sets
                determines the output_ports of the Conditional
                according to its internal components.
            If all no branch Predicate evaluats to True, then pass
                input Ports to outputs and new Ports have undefined
                values.
    """
    # branches is a List of
    #   ( <Predicate>1, <Function>, [<UidWire>+] )
    branches: List[Tuple[Union[Predicate, None],
                         Function,
                         List[UidWire]]]


@dataclass
class Loop(BoxDirected, HasContents):
    """
    Loop
        ( TODO:
            Assumes no side-effects.
            Assumes no breaks.
        )
    A BoxDirected that "loops" until an exit_condition (Predicate)
        is True.
        By "loop", you can think of iteratively making a copies of
            the Loop and wiring the previous Loop instance output_ports
            to the input_ports of the next Loop instance.
            (wiring of output-to-input Ports is done is order
             of the Ports).
    Definition / Terminology:
        A Loop has a *body* (because it is a Box), that
            represents the "body" of the loop.
        A Loop has an *exit_condition*, a Predicate that
            determines whether to evaluate the loop.
        A Loop has input_ports and output_ports (being
            a BoxDirected).
            A portion of the input_ports represent Ports
                set by the incoming external "environment"
                of the Loop.
            The remaining of the input_ports represent
                Ports to store state values that may be
                introduced within the Loop body
                but are not themselves initially used in
                (read by) the loop body wiring.
                In the initial evaluation of the loop,
                these Ports have no values; after one
                iteration of the Loop, these Ports
                may have their values assigned by the
                Loop body.
        Each input_port is "matched" to an output_port,
            based on the Port order within the input_ports
            and output_ports lists.
        A Loop has a *port_map* is a bi-directional map
            that pairs each Loop output Port with each Loop
            input Port, determining what the Loop input Port
            value will be based on the previous Loop iteration.
            Some input Port values will not be changed as a
            result of the Loop body, so these values "pass
            through" to that input's paired output.
            Others may be changed by the Loop body evaluation.
    Interpretation:
        The Loop exit_condition is evaluated at the very
            beginning before evaluating any of the Loop
            body wiring.
            IF True (the exit_condition evaluates to True),
                then the values of the Ports in input_ports
                are passed directly to their corresponding
                Ports in output_ports; The output_ports then
                represent the final value/state of the Loop
                output_ports.
            IF False (the exit_condition evaluates to False),
                then the Loop body wiring is evaluated to
                determine the state of each output Port value.
                The values of each output Port are then assined
                to the Port's corresponding input Port and
                the next Loop iteration is begun.
        This basic semantics supports both standard loop
            semantics:
            () while: the exit_condition is tested first.
            () repeat until: an initial input Port set to False
                make the initial exit_condition evaluation fail
                and is thereafter set to True in the Loop body.
    """
    exit_condition: Union[Predicate, None]


# --------------------
# Variable

@dataclass
class Variable(TypedGrometElm):
    """
    A Variable is the locus of two representational roles:
        (a) denotes one or more elements that are Valued,
            i.e., carry a value (aka: states) and
        (b) denotes a modeled domain (world) state.
    Currently, (b) will be represented in Metadata.

    """
    uid: UidVariable
    name: str
    states: List[Union[UidPort, UidWire, UidJunction]]
    metadata: Metadata


# --------------------
# Gromet top level

@dataclass
class Gromet(TypedGrometElm):
    uid: UidGromet
    name: Union[str, None]
    root: Union[UidBox, None]
    types: Union[List[TypeDeclaration], None]
    ports: Union[List[Port], None]
    wires: Union[List[Wire], None]
    boxes: List[Box]
    variables: Union[List[Variable], None]
    metadata: Metadata


'''
@dataclass
class Measure(GrometElm):
    wire: Wire
    interval: ???: Tuple or Array
    type: Type  # Enum("instance", interval, steady_state)
'''


# -----------------------------------------------------------------------------
# Utils
# -----------------------------------------------------------------------------

def gromet_to_json(gromet: Gromet, dst_file: Union[str, None] = None):
    if dst_file is None:
        dst_file = f"{gromet.name}.json"
    json.dump(asdict(gromet),  # gromet.to_dict(),
              open(dst_file, "w"),
              indent=2)


# -----------------------------------------------------------------------------
# CHANGE LOG
# -----------------------------------------------------------------------------

"""
Changes 2021-05-17:
() FOR NOW: commenting out much of the Types, as likely source of
    confusion until sorted out.
() Added HasContents as a "mixin" that provides explicit lists
    of junctions, boxes, and wires.
    This is mixed-in to: Loop, Function and Relation.
() Added Valued class, a type of TypedGrometElm, that introduced
    the attributes of "value" (i.e., for things that can carry
    a value). This is now the parent to Junction, Port and Wire.
    This also distinguishes those classes from Box, which does
        not have a value, but is intended to transform or assert
        relationships between values.
() Changes to Loop:
    Removed "port_map" -- the pairing of input and output Ports
        is now based on the order of Ports in the input_ports and
        output_ports lists.
    Cleaned up documentation to reflect this.

Changes [2021-05-09 to 2021-05-16]:
() Added parent class TypedGrometElm inherited by any GrometElm that
    has a type. GrometElm's with types play general model structural roles,
    while other non-typed GrometElms add element-specific structure (such
    as Expr, RefFn, RefOp, Type, etc...)
() UidOp will now be reserved ONLY for primitive operators that are not
    explicitly defined within the gromet.
    All other "implementations" of transformations must have associated
        Box definitions with UidBox uids
() Introduced RefOp and RefFn to explicitly distinguish between the two
() Exp renamed to Expr
() Expr field "operator" -> "call", where type is now either RefOp or RefFn
() Expression changed from being a child of Function to being child of BoxDirected
() Changed Predicate to being an Expression
() Added Conditional, child of BoxDirected
() Added Loop, child of BoxDirected
() WireUndirected
    ports changed from List[Union[UidPort, UidJunction]]
    to Union[Tuple[UidPort, UidJunction],
             Tuple[UidJunction, UidPort],
             Tuple[UidPort, UidPort]]
    - should only have one pairwise connection per UndirectedWire

"""
