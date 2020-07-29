import sys, re, os, argparse
from templates.courses import courses

SCRIPT_DIRNAME=os.path.dirname(os.path.realpath(__file__))

def copy_file(filename, new_name=""):
    with open("{}/templates/{}".format(SCRIPT_DIRNAME, filename),"r") as template:
        alt_name = new_name+os.path.splitext(filename)[1]
        out_name = alt_name if new_name else filename
        with open(out_name,"w+") as out:
            for line in template:
                out.write(line)

def list_course_ids(_semester):
    print("Listing all valid COURSE_IDs for semester {}:".format(_semester))
    for semester, info in courses["SEMESTER"].iteritems():
        if _semester == semester or _semester == "ALL":
            print("======")
            print(semester)
            print("======")
            for course_id, course_info in info["COURSE_ID"].iteritems():
                print("{}: {}, {}".format(course_id,\
                        course_info["COURSE_NUMBER"],\
                        course_info["COURSE_NAME"]))

def create_template(template_file, output_file_name, replace_dict):
    with open(output_file_name+".latexmain",'a'):
        # Create the main file indicator
        os.utime(output_file_name+".latexmain", None)
    with open("{}/templates/{}".format(SCRIPT_DIRNAME,template_file),"r") as template:
        with open(output_file_name + ".tex","w+") as out:
            for line in template:
                for key, val in replace_dict.items():
                    line = line.replace(key, val)
                out.write(line)

def create_hw_template(template_file, semester, course_id, pset_number, due_date, collaborators, course_info):
    course_number = course_info["COURSE_NUMBER"]
    course_name = course_info["COURSE_NAME"]
    instr_names = course_info["INSTRUCTOR_NAMES"]
    anonymous = course_info.get("ANONYMOUS")
    if course_name == "" or instr_names == "":
        print("Missing course name or instructor name in course_info! Cannot continue")
        sys.exit(1)
    else:
        print("Determined course name: {} and instructor(s): {}".format(course_name, instr_names))
    multiple_instructors = instr_names.count(',') > 0
    output_file_name = "ps{}_{}_{}".format(pset_number, \
            course_number.replace(" ","_"), \
            re.sub(r'[\s,]+','_',semester))

    create_template(template_file=template_file,
            output_file_name=output_file_name,
            replace_dict={
                "<ASSIGNMENT_NUMBER>": pset_number,
                "<SEMESTER>": semester,
                "<COURSE_ID>": course_number,
                "<INSTRUCTOR_PLURAL>": "s" if multiple_instructors else "",
                "<INSTRUCTOR_NAMES>": instr_names,
                "<NAME>": "Anonymous" if anonymous else "Matthew Faw",
                "<DUE_DATE>": due_date,
                "<COLLABORATORS>": "Collaborators (in "
                        +"accordance with the course collaboration policy): "
                        +"{}\\\\".format(collaborators) if collaborators != "" else ""
                })

def create_paper_template(template_file, title, output_file_name):
    create_template(template_file=template_file,
            output_file_name=output_file_name,
            replace_dict={"<TITLE>": title,
                "<FNAME>": output_file_name
                })

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Create a template")
    parser.add_argument("--list", action='store_true')
    parser.add_argument("--generate-hw", action='store_true')
    parser.add_argument("--generate-paper", action='store_true')
    parser.add_argument("--semester", type=str, default="ALL", required=False,
            help="The semester to list courses. Only used when listing courses")
    parser.add_argument("--course-id", type=str, default="", required=False,
            help="The course id in courses.py")
    parser.add_argument("--pset-number", type=str, default="", required=False,
            help="The problem set number")
    parser.add_argument("--due-date", type=str, default="", required=False,
            help="The problem set due date")
    parser.add_argument("--collaborators", type=str, default="", required=False,
            help="Comma separated list of collaborators")
    parser.add_argument("--title", type=str, default="", required=False,
            help="Title for paper")
    args = parser.parse_args()

    if args.list:
        list_course_ids(args.semester)
    elif args.generate_hw:
        made_template = False
        for semester in courses["SEMESTER"].iterkeys():
            for course_id, course_info in courses["SEMESTER"][semester]["COURSE_ID"].iteritems():
                if args.course_id == course_id:
                    print("Creating template for {} {}".format(semester,course_id))
                    create_hw_template(template_file="hw_template_2.tex",
                            semester=semester,
                            course_id=course_id,
                            pset_number=args.pset_number,
                            due_date=args.due_date,
                            collaborators=args.collaborators,
                            course_info=course_info)
                    copy_file("mfhw.sty")
                    copy_file("p1.tex")
                    made_template = True

        if not made_template:
            print("Failed to find course_info for course id: {}".format(args.course_id))
            sys.exit(1)
    elif args.generate_paper:
        print("Creating paper titled {}".format(args.title))
        output_file_name = re.sub('[\ :]', '-', args.title).lower()
        create_paper_template(template_file="research-template.tex",
                title=args.title,
                output_file_name=output_file_name)
        copy_file("research-template.sty", new_name=output_file_name)
        copy_file("abstract.tex")
        copy_file("body.tex")
        copy_file("research-template.bib", new_name=output_file_name)
        copy_file("appendix.tex")
    else:
        print("No function specified -- cannot proceed")
        sys.exit(1)
