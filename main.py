import sys
import time

from utils import get_daily_papers_by_keyword_with_retries, generate_table, back_up_file, get_daily_date


# keywords
keywords = ["Open Vocabulary Semantic Segmentation", "Remote Sensing Segmentation", "Remote Sensing Vision Language Model", "Vision Language Model"] # TODO add more keywords

max_result = 100 # maximum query results from arXiv API for each keyword
issues_result = 15 # maximum papers to be included in the issue

# all columns: Title, Link, Abstract, Date, Tags, Comment
column_names = ["Title", "Link", "Abstract", "Date", "Comment"]

all_papers = {}

for keyword in keywords:
    if len(keyword.split()) == 1:
        link = "AND" # for keyword with only one word, We search for papers containing this keyword in both the title and abstract.
    else:
        link = "OR"
    papers = get_daily_papers_by_keyword_with_retries(keyword, column_names, max_result, link)
    if papers is not None:
        all_papers[keyword] = papers

if len(all_papers) == 0:
    print("No paper found!")
    sys.exit("No paper found!")

cur_date = get_daily_date()

f_rm = open("README.md", "w", encoding="utf-8")
f_is = open(".github/ISSUE_TEMPLATE.md", "w", encoding="utf-8")

f_rm.write("# Daily Papers\n")

f_is.write("---\n")
f_is.write("title: Papers - {0}\n".format(cur_date))
f_is.write("labels: documentation\n")
f_is.write("---\n")

for keyword in keywords:
    if keyword not in all_papers:
        f_rm.write("## {0} - No Paper Found\n".format(keyword))
        f_is.write("## {0} - No Paper Found\n".format(keyword))
        continue

    f_rm.write("## {0} - {1} in Total\n".format(keyword, len(all_papers[keyword])))
    f_is.write("## {0} - Preview {1} papers\n".format(keyword, len(all_papers[keyword][:issues_result])))
    
    rm_table = generate_table(all_papers[keyword])
    is_table = generate_table(all_papers[keyword][:issues_result], ignore_keys=["Abstract"])
    f_rm.write(rm_table)
    f_rm.write("\n\n")
    f_is.write(is_table)
    f_is.write("\n\n")
    time.sleep(5) # avoid being blocked by arXiv API

f_rm.close()
f_is.close()

f = open("backup/q.md", "w", encoding="utf-8")
f.write(111111)
f.close()


# back_up_file("README.md", cur_date)
