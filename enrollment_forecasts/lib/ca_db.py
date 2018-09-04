#!/usr/local/bin/python

from sqlalchemy import create_engine, text

class CaDb:

  def __init__ (self):
    # Create an engine to the census database
    self.db = create_engine('mysql+pymysql://root:&$#$JFl23asfjA)8wfLFr29&^@localhost/CaliforniaEnrollment')

  def getDistricts(self):
    # THIS IS THE DISTRICT I INITALLY WORKED WITH: ROSS VALLEY
    sql = "SELECT * FROM Districts d WHERE d.id = 290"

    # THIS IS ALL OF THE DISTRICTS
    sql = "SELECT d.id as districtId, d.name as districtName FROM Districts d"

    # NOT ENOUGH DATA TO CALCULATE THIS
    #sql = "SELECT * FROM Districts d WHERE d.id = 35"

    result = self.db.engine.execute(text(sql))
    return result

  def getDistrict(self, districtId):
    sql = "SELECT * FROM Districts d WHERE d.id = " + str(districtId)
    result = self.db.engine.execute(text(sql))
    return result

  def getSchoolGradeCounts(self, districtId):
    sql = "SELECT year, sum(kdgn) as 'K', sum(gr_1) as '1', sum(gr_2) as '2', sum(gr_3) as '3', sum(gr_4) as '4', sum(gr_5) as '5', sum(gr_6) as '6', sum(gr_7) as '7', sum(gr_8) as '8', sum(gr_9) as '9', sum(gr_10) as '10', sum(gr_11) as '11', sum(gr_12) as '12' FROM Districts d JOIN Schools s ON s.district_id = d.id JOIN SchoolGradeCounts c ON c.school_id = s.id WHERE d.id =" + str(districtId) + " GROUP BY d.id, year LIMIT 6"

    result = self.db.engine.execute(text(sql))
    return result

