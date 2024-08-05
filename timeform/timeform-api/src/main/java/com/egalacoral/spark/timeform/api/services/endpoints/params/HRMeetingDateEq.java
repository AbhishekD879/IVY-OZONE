package com.egalacoral.spark.timeform.api.services.endpoints.params;

import com.egalacoral.spark.timeform.api.tools.Tools;
import java.text.DateFormat;
import java.util.Date;

/** Created by llegkyy on 31.08.16. */
public class HRMeetingDateEq extends FilterParamValue<Date> {
  private static final String MEETING_DATE_EXPR = "meetingDate eq datetime'%s'";

  public HRMeetingDateEq(Date value) {
    super(MEETING_DATE_EXPR, value);
  }

  public HRMeetingDateEq(String paramsExpr, Date value) {
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
