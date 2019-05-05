# encoding=utf8
# fichier permettant dexporter vers csv les item id et item name
import sys
import csv
import datetime
import mysql.connector
from decimal import Decimal


# Connect to MSSQL Server
try:
    conn = mysql.connector.connect(host="localhost", user="root",password="", database="wow")
    print('connected')
except:
    print('error')
# Create a database cursor
cursor = conn.cursor()

# Replace this nonsense with your own query :)
# query = """SELECT entry,Title, Details, Objectives, Method, MinLevel, QuestLevel, PrevQuestId, NextQuestId, NextQuestInChain,
# OfferRewardText, LimitTime, SuggestedPlayers,
# SrcItemId, SrcItemCount, SrcSpell,
# RequiredClasses, RequiredRaces,
# RequiredSkill, RequiredSkillValue, RepObjectiveFaction, RepObjectiveValue,
# RequiredMinRepFaction, RequiredMinRepValue, RequiredMaxRepFaction, RequiredMaxRepValue,
# ReqItemId1, ReqItemId2, ReqItemId3, ReqItemId4, ReqItemCount1, ReqItemCount2, ReqItemCount3, ReqItemCount4,
# ReqCreatureOrGOId1, ReqCreatureOrGOId2, ReqCreatureOrGOId3, ReqCreatureOrGOId4,
# ReqCreatureOrGOCount1, ReqCreatureOrGOCount2, ReqCreatureOrGOCount3, ReqCreatureOrGOCount4,
# ReqSpellCast1, ReqSpellCast2, ReqSpellCast3, ReqSpellCast4,
# RewChoiceItemId1, RewChoiceItemId2, RewChoiceItemId3, RewChoiceItemId4, RewChoiceItemId5, RewChoiceItemId6,
# RewChoiceItemCount1, RewChoiceItemCount2, RewChoiceItemCount3, RewChoiceItemCount4, RewChoiceItemCount5, RewChoiceItemCount6,
# RewItemId1, RewItemId2, RewItemId3, RewItemId4,
# RewItemCount1, RewItemCount2, RewItemCount3, RewItemCount4
# RewRepFaction1, RewRepFaction2, RewRepFaction3, RewRepFaction4, RewRepFaction5,
# RewRepValue1, RewRepValue2, RewRepValue3, RewRepValue4, RewRepValue5,
# RewOrReqMoney, RewMoneyMaxLevel,
# RewSpell, RewSpellCast
#  FROM quest_template"""

query = """SELECT * FROM playercreateinfo_spell"""

# Execute the query
cursor.execute(query)

# Go through the results row-by-row and write the output to a CSV file
# (QUOTE_NONNUMERIC applies quotes to non-numeric data; change this to
# QUOTE_NONE for no quotes.  See https://docs.python.org/2/library/csv.html
# for other settings options)
with open("playerinfospells.csv", "w",newline='') as outfile:
    writer = csv.writer(outfile, delimiter=',')
    writer.writerow([i[0] for i in cursor.description])
    for row in cursor:
        if not row:
            continue
        writer.writerow(row)

# Close the cursor and the database connection
cursor.close()
conn.close()
