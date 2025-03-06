import json
import re

from configs.paths import SPIDER_DEV_PATH, BIRD_DEV_PATH



def get_dev_dbs(dataset:str = "spider"):

    if dataset == "spider":
        p = SPIDER_DEV_PATH
    elif dataset == "bird":
        p = BIRD_DEV_PATH

    with open(p, "r") as f:
        dev = json.load(f)
    
    db_ids = list()
    for d in dev:
        db_ids.append(d["db_id"])

    return set(db_ids)



def extract_snippet(txt:str, start: str, end:str): # general text extraction
    
    start_pos = txt.index(start) + len(start)
    end_pos = txt.index(end, start_pos)
    res = txt[start_pos:end_pos].strip()
    
    return res


def extract_sql(res: str): # extract sql from response
    s = "```sql\n"
    e = "```"
    sql = extract_snippet(res, s, e)
    return sql.replace("\n", " ")

def remove_comments(sql: str): # remove comments from sql
    s = "--"
    e = "\n"

    while "--" in sql:        
        start_pos = sql.index(s)
        end_pos = sql.index(e, start_pos) + len(e)

        sql = sql[:start_pos] + sql[end_pos:]

    return sql

def clean_sql(sql: str): # other cleanings to sql
    sql = sql.replace("\n", " ")
    sql = " ".join(sql.split())
    return sql

def remove_aliases(sql_query: str):
    start = "SELECT"
    end = "FROM"
    start_pos = sql_query.index(start) + len(start)
    end_pos = sql_query.index(end, start_pos)

    select = sql_query[start_pos:end_pos].strip()
    # Regular expression to match aliases in the SELECT part of the SQL query
    alias_pattern = re.compile(r' AS \w+', re.IGNORECASE)
    # Removing the aliases by substituting with an empty string
    select = alias_pattern.sub('', select)

    sql = "SELECT " + select + " " + sql_query[end_pos:]
    
    return sql