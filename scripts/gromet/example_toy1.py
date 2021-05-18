from gromet import *  # never do this :)


# -----------------------------------------------------------------------------
# GroMEt instance: toy1
# -----------------------------------------------------------------------------

def toy1_example() -> Gromet:

    ports = [
        # input ports to 'toy1'
        Port(uid=UidPort("P:toy1.in.x"), box=UidBox("B:toy1"),
             type=UidType("T:Float"), name="x", value=None, metadata=None),
        Port(uid=UidPort("P:toy1.in.y"), box=UidBox("B:toy1"),
             type=UidType("T:Int"), name="y", value=None, metadata=None),
        # output ports to 'toy1'
        Port(uid=UidPort("P:toy1.out.x"), box=UidBox("B:toy1"),
             type=UidType("T:Float"), name="x1", value=None, metadata=None),
        Port(uid=UidPort("P:toy1.out.z"), box=UidBox("B:toy1"),
             type=UidType("T:Float"), name="x1", value=None, metadata=None),

        # input ports to 'toy1_set_z_exp'
        Port(uid=UidPort("P:toy1_set_z_exp.in.x"), box=UidBox("B:toy1_set_z_exp"),
             type=UidType("T:Float"), name="x", value=None, metadata=None),
        Port(uid=UidPort("P:toy1_set_z_exp.in.y"), box=UidBox("B:toy1_set_z_exp"),
             type=UidType("T:Float"), name="y", value=None, metadata=None),
        # output ports to 'toy1_set_z_exp'
        Port(uid=UidPort("P:toy1_set_z_exp.out.z"), box=UidBox("B:toy1_set_z_exp"),
             type=UidType("T:Float"), name="z", value=None, metadata=None),

        # input ports to 'toy1_reset_x_exp'
        Port(uid=UidPort("P:toy1_reset_x_exp.in.z"), box=UidBox("B:toy1_reset_x_exp"),
             type=UidType("T:Float"), name="z", value=None, metadata=None),
        # output ports to 'toy1_reset_x_exp'
        Port(uid=UidPort("P:toy1_reset_x_exp.out.x"), box=UidBox("B:toy1_reset_x_exp"),
             type=UidType("T:Float"), name="x", value=None, metadata=None),

        # input ports to 'add1'
        Port(uid=UidPort("P:add1.in.x"), box=UidBox("B:add1"),
             type=UidType("T:Float"), name="x", value=None, metadata=None),
        # output ports to 'add1'
        Port(uid=UidPort("P:add1.out.result"), box=UidBox("B:add1"),
             type=UidType("T:Float"), name=None, value=None, metadata=None),

        # input ports to 'add1'
        Port(uid=UidPort("P:add1_exp.in.x"), box=UidBox("B:add1_exp"),
             type=UidType("T:Float"), name="x", value=None, metadata=None),
        # output ports to 'add1'
        Port(uid=UidPort("P:add1_exp.out.result"), box=UidBox("B:add1_exp"),
             type=UidType("T:Float"), name=None, value=None, metadata=None),
    ]

    wires = [
        WireDirected(uid=UidWire("W:add1_x"), type=UidType("T:Float"),
                     name=None, value=None, metadata=None,
                     input=UidPort("P:add1.in.x"),
                     output=UidPort("P:add1_exp.in.x")),
        WireDirected(uid=UidWire("W:add1_result"), type=UidType("T:Float"),
                     name=None, value=None, metadata=None,
                     input=UidPort("P:add1_exp.out.result"),
                     output=UidPort("P:add1.out.result")),
        WireDirected(uid=UidWire("W:toy1_x"), type=UidType("T:Float"),
                     name=None, value=None, metadata=None,
                     input=UidPort("P:toy1.in.x"),
                     output=UidPort("P:toy1_set_z_exp.in.x")),
        WireDirected(uid=UidWire("W:toy1_y"), type=UidType("T:Int"),
                     name=None, value=None, metadata=None,
                     input=UidPort("P:toy1.in.y"),
                     output=UidPort("P:toy1_set_z_exp.in.y")),
        WireDirected(uid=UidWire("W:toy1_set_z1"), type=UidType("T:Float"),
                     name=None, value=None, metadata=None,
                     input=UidPort("P:toy1_set_z_exp.out.z"),
                     output=UidPort("P:toy1_reset_x_exp.in.z")),
        WireDirected(uid=UidWire("W:toy1_set_z2"), type=UidType("T:Float"),
                     name=None, value=None, metadata=None,
                     input=UidPort("P:toy1_set_z_exp.out.z"),
                     output=UidPort("P:toy1.out.z")),
        WireDirected(uid=UidWire("W:toy1_reset_x"), type=UidType("T:Float"),
                     name=None, value=None, metadata=None,
                     input=UidPort("P:toy1_reset_x_exp.out.x"),
                     output=UidPort("P:toy1.out.x")),
    ]

    # ====================
    # Boxes

    # ----------
    # add1

    # Expression add1_exp
    # Expr's
    e3 = Expr(call=RefOp(UidOp("+")),
              args=[UidPort("P:add1_exp.in.x"),
                    Literal(uid=None, type=UidType("Int"), value=Val("1"), metadata=None)])
    # the anonymous Expression
    add1_exp = Expression(uid=UidBox("B:add1_exp"),
                          type=None,
                          name=None,
                          input_ports=[UidPort("P:add1_exp.in.x")],
                          output_ports=[UidPort("P:add1_exp.out.result")],
                          tree=e3,
                          metadata=None)

    add1 = Function(uid=UidBox("B:add1"),
                    type=None,
                    name=UidFn("F:add1"),
                    input_ports=[UidPort("P:add1.in.x")],
                    output_ports=[UidPort("P:add1.out.result")],

                    # contents
                    wires=[UidWire("W:add1_x"), UidWire("W:add1_result")],
                    boxes=[UidBox("B:add1_exp")],
                    junctions=None,

                    metadata=None)

    # ----------
    # toy1

    # Expression toy1_set_z
    # Expr's
    e1 = Expr(call=RefOp(UidOp("*")),
              args=[UidPort("P:toy1_set_z_exp.in.x"),
                    UidPort("P:toy1_set_z_exp.in.y")])
    # the anonymous (no name) Expression
    toy1_set_z_exp = \
        Expression(uid=UidBox("B:toy1_set_z_exp"),
                   type=None,
                   name=None,
                   input_ports=[UidPort("P:toy1_set_z_exp.in.x"),
                                UidPort("P:toy1_set_z_exp.in.y")],
                   output_ports=[UidPort("P:toy1_set_z_exp.out.z")],
                   tree=e1,
                   metadata=None)

    # Expression reset_x
    # Expr's
    e2 = Expr(call=RefFn(UidFn("F:add1")),
              args=[UidPort("P:toy1_reset_x_exp.in.z")])
    # the anonymous (no name) Expression
    toy1_reset_x_exp = \
        Expression(uid=UidBox("B:toy1_reset_x_exp"),
                   type=None,
                   name=None,
                   input_ports=[UidPort("P:toy1_reset_x_exp.in.z")],
                   output_ports=[UidPort("P:toy1_reset_x_exp.out.x")],
                   tree=e2,
                   metadata=None)

    toy1 = Function(uid=UidBox("B:toy1"),
                    type=None,
                    name=UidBox("toy1"),
                    input_ports=[UidPort("P:toy1.in.x"), UidPort("P:toy1.in.y")],
                    output_ports=[UidPort("P:toy1.out.x"), UidPort("P:toy1.out.z")],

                    # contents
                    wires=[UidWire("W:toy1_x"), UidWire("W:toy1_y"),
                           UidWire("W:toy1_set_z1"), UidWire("W:toy1_set_z2"),
                           UidWire("W:toy1_reset_x")],
                    boxes=[UidBox("B:toy1_set_z_exp"),
                           UidBox("B:toy1_reset_x_exp")],
                    junctions=None,

                    metadata=None)

    boxes = [toy1, toy1_set_z_exp, toy1_reset_x_exp,
             add1, add1_exp]

    variables = [
        Variable(uid=UidVariable("var1"), name="x", type=UidType("Float"),
                 states=[UidWire("W:toy1_x")],
                 metadata=None),
        Variable(uid=UidVariable("var2"), name="y", type=UidType("Float"),
                 states=[UidWire("W:toy1_y")],
                 metadata=None),
        Variable(uid=UidVariable("var3"), name="z", type=UidType("Float"),
                 states=[UidWire("W:toy1_set_z")],
                 metadata=None),
        Variable(uid=UidVariable("var4"), name="x", type=UidType("Float"),
                 states=[UidWire("W:toy1_reset_x")],
                 metadata=None)
    ]

    g = Gromet(
        uid=UidGromet("toy1"),
        name="toy1",
        type=UidType("FunctionNetwork"),
        root=toy1.uid,
        types=None,
        ports=ports,
        wires=wires,
        boxes=boxes,
        variables=variables,
        metadata=None
    )

    return g


# -----------------------------------------------------------------------------
# Script
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    gromet_to_json(toy1_example())
