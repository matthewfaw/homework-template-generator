import sys, re, os
from templates.courses import courses

SCRIPT_DIRNAME=os.path.dirname(os.path.realpath(__file__))

F_LIST = "list"
F_GENERATE = "generate"
function = ""
TEX_TEMPLATE_FILE = "hw_template_2.tex"

if len(sys.argv) >= 2 and sys.argv[1] == F_LIST:
    function = F_LIST
elif len(sys.argv) == 5:
    function = F_GENERATE
else:
    print "Required arguments are either:"
    print "a) COURSE_ID PSET_NUMBER DUE_DATE COLLABORATORS (to generate LaTeX template)"
    print "or"
    print "b) list [SEMESTER] (to list all valid COURSE_IDs)"
    sys.exit(1)

def copy_file(filename):
    with open("%s/templates/%s" % (SCRIPT_DIRNAME, filename),"r") as template:
        with open("%s" % (filename),"w+") as out:
            for line in template:
                out.write(line)

def create_template(semester, course_id, pset_number, due_date, collaborators, course_info):
    course_number = course_info["COURSE_NUMBER"]
    course_name = course_info["COURSE_NAME"]
    instr_names = course_info["INSTRUCTOR_NAMES"]
    anonymous = course_info.get("ANONYMOUS")
    if course_name == "" or instr_names == "":
        print("Missing course name or instructor name in course_info! Cannot continue")
        sys.exit(1)
    else:
        print "Determined course name: %s and instructor(s): %s" % \
                (course_name, instr_names)
    multiple_instructors = instr_names.count(',') > 0
    output_file_name = "ps%s_%s_%s" % (pset_number, \
            course_number.replace(" ","_"), \
            re.sub(r'[\s,]+','_',semester))
    with open(output_file_name+".latexmain",'a'):
        # Create the main file indicator
        os.utime(output_file_name+".latexmain", None)
    with open("%s/templates/%s" % (SCRIPT_DIRNAME,TEX_TEMPLATE_FILE),"r") as template:
        with open(output_file_name + ".tex","w+") as out:
            for line in template:
                line = line.replace("<ASSIGNMENT_NUMBER>",pset_number)
                line = line.replace("<SEMESTER>",semester)
                line = line.replace("<COURSE_ID>",course_number)
                line = line.replace("<INSTRUCTOR_PLURAL>","s" if multiple_instructors else "")
                line = line.replace("<INSTRUCTOR_NAMES>",instr_names)
                line = line.replace("<NAME>", "Anonymous" if anonymous \
                        else "Matthew Faw")
                line = line.replace("<DUE_DATE>",due_date)
                line = line.replace("<COLLABORATORS>", "Collaborators (in "
                        +"accordance with the course collaboration policy): "
                        +"{}\\\\".format(collaborators) if collaborators != "" else "")
                out.write(line)

def list_course_ids(_semester):
    print "Listing all valid COURSE_IDs for semester %s:" % (_semester)
    for semester, info in courses["SEMESTER"].iteritems():
        if _semester == semester or _semester == "ALL":
            print "======"
            print semester
            print "======"
            for course_id, course_info in info["COURSE_ID"].iteritems():
                print "%s: %s, %s" % (course_id,\
                        course_info["COURSE_NUMBER"],\
                        course_info["COURSE_NAME"])

if function == F_LIST:
    semester = "ALL"
    if len(sys.argv) > 2:
        semester = sys.argv[2]

    list_course_ids(semester)
elif function == F_GENERATE:
    target_course_id=sys.argv[1]
    pset_number=sys.argv[2]
    due_date=sys.argv[3]
    collaborators=sys.argv[4]

    made_template = False
    for semester in courses["SEMESTER"].iterkeys():
        for course_id, course_info in courses["SEMESTER"][semester]["COURSE_ID"].iteritems():
            if target_course_id == course_id:
                print("Creating template for %s %s" % (semester,course_id))
                create_template(semester, course_id, pset_number, due_date, collaborators, course_info)
                copy_file("mfhw.sty")
                copy_file("p1.tex")
                made_template = True

    if not made_template:
        print("Failed to find course_info for course id: %s"%(target_course_id))
        sys.exit(1)
