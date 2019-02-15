import os, glob
import tarfile
import argparse
import subprocess


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('tarball') # the path with the arxiv arXiv_src_*_*.tar files
    parser.add_argument('outputdir')  # the path to store the expanded dirs
    parser.add_argument('--keepall', action='store_true', default=False) # set to true to keep tarballs and pdfs
    parser.add_argument('--verbose', action='store_true', default=False)
    args = parser.parse_args()
    return args

def is_pdf(f):
    return f.endswith(".pdf")

def is_gz(f):
    return f.endswith(".gz")

# gunzip file, return name of uncompressed file
def gunzip_file(f):
    try:
        # gunzip(f)
        subprocess.check_call(['gunzip', f])
    except:
        print "WARNING: Didn't unzip, check to make sure the file ({0}) wasn't already uncompressed".format(f)
    return f[:-3]  # the name after gunzip

# make a directory for the paper file(s), return path
def mk_paper_dir(f):
    paper_dir = f + "_dir"
    if not os.path.exists(paper_dir):
        os.makedirs(paper_dir)
        return paper_dir
    else:
        return None

def rename_file(paperdir):
    new_path = paperdir[:-4]
    os.rename(paperdir, new_path)


# wdir: the path with the arxiv arXiv_src_*_*.tar files
def expand_arxiv(fn, outdir, keep_all, verbose):

    print "Extracting files from", fn
    assert(tarfile.is_tarfile(fn) == True) # for good measure...
    tar = tarfile.open(fn)
    extracted_files = tar.getnames() # files to extract
    print(','.join(extracted_files))
    # check to see if they are already extracted
    # need_to_extract = 0
    # for to_extract in extracted_files:
    #     path_to_check = os.path.join(outdir, to_extract)
    #     if not os.path.exists(path_to_check):
    #         need_to_extract = 1

    tar.extractall(path=outdir)
    tar.close()

    file_counter = 0
    for f in extracted_files:
        # path to the extracted file that needs to be handled
        f = os.path.join(outdir, f)

        # We expect that this file will be a gzipped file or a pdf
        # If it's a gzipped file (i.e., with latex source):
        if is_gz(f):
            file_counter += 1
            # gunzip it, return newly uncompressed filename
            base_path = gunzip_file(f)
            # make dir where paper contents will go
            paper_dir = mk_paper_dir(base_path)
            # If the paper directory was already made, then we're done here
            if paper_dir == None:
                print("Paper", base_path, "already processed")
                return 0

            # Either the uncompressed file will be a tar file or a single tex file (w/o the tex extension!)
            # Case 1: if it's a tar file
            if tarfile.is_tarfile(base_path):
                # untar it to the paper directory
                paper_tar = tarfile.open(base_path)
                paper_tar.extractall(path=paper_dir)
                paper_tar.close()
                # Remove the tar file
                if not keep_all:
                    subprocess.check_call(['rm', base_path])

            # Case 2: it's the tex file missing its extension
            else:
                # rename it and move to the paper dir
                base_name = os.path.split(base_path)[1]
                tex_path = os.path.join(paper_dir, base_name + ".tex")
                os.rename(base_path, tex_path)

            # Rename the directory
            rename_file(paper_dir)

        # Otherwise, if it's a pdf, disregard
        elif is_pdf(f):
            if not keep_all:
                subprocess.check_call(['rm', f])
        # There are a few other formats, we also will disregard them, but just in case we want to see
        # how many and of what type...
        else:
            if verbose:
                print "INFO: didn't handle file ", f
            # not removing here bc we get the main dir in the list, I guess bc of the api for
            # tarfile.getnames()...
    if verbose:
        print "... finished extracting {0} papers".format(file_counter)

    return file_counter




if __name__ == '__main__':
    args = parse_args()
    if not os.path.exists(args.outputdir):
        os.makedirs(args.outputdir)

    # expand the initial files, e.g., arXiv_src_1808_023.tar
    handled = expand_arxiv(args.tarball, args.outputdir, args.keepall, args.verbose)


    print "  ... {0} arxiv papers expanded".format(handled)

