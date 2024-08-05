package com.egalacoral.spark.timeform.api.services.endpoints.params;

import com.egalacoral.spark.timeform.api.tools.Tools;
import java.text.DateFormat;
import java.util.Date;

public class MeetingDateEq extends FilterParamValue<Date> {

  private static final String MEETING_DATE_EXPR = "meeting_date eq datetime'%s'";

  public MeetingDateEq(Date value) {
    super(MEETING_DATE_EXPR, value);
  }

  public MeetingDateEq(String paramsExpr, Date value) {
    super(build(paramsExpr), value);
  }

  private static String build(String pramsExpr) {
    StringBuilder sb = new StringBuilder();
    return sb.append(pramsExpr).append(MEETING_DATE_EXPR).toString();
  }

  @Override
  protected Object formatValue() {
    DateFormat df = Tools.simpleDateFormat("yyyy-MM-dd");
    return df.format(getValue());
  }
}
