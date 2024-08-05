package com.egalacoral.spark.timeform.api.services.endpoints.params;

import com.egalacoral.spark.timeform.api.tools.Tools;
import java.text.DateFormat;
import java.util.Date;

public class MeetingDateAfter extends FilterParamValue<Date> {

  private static final String MEETING_DATE_AFTER = "meeting_date gt datetime'%s'";

  public MeetingDateAfter(Date value) {
    super(MEETING_DATE_AFTER, value);
  }

  public MeetingDateAfter(String paramsExpr, Date value) {
    super(build(paramsExpr), value);
  }

  private static String build(String pramsExpr) {
    StringBuilder sb = new StringBuilder();
    return sb.append(pramsExpr).append(MEETING_DATE_AFTER).toString();
  }

  @Override
  protected Object formatValue() {
    DateFormat df = Tools.simpleDateFormat("yyyy-MM-dd");
    return df.format(getValue());
  }
}
