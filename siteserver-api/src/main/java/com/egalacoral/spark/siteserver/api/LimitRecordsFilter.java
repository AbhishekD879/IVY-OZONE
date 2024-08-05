package com.egalacoral.spark.siteserver.api;

import java.util.ArrayList;
import java.util.List;

/**
 * LimitRecords filter may be specified by the client on certain requests to reduce the total number
 * of records returned in the SiteServer response. An example of a LimitRecords filter parameter is:
 * ...&limitRecords=market:5 This could be used on a /EventToMarketForClass request to specify that
 * a maximum five markets should be return per event.
 *
 * <ul>
 *   <li>This filter restricts records based on specified limit and parent record, ie Setting market
 *       limit of 5 will output a maximum of 5 market records per event.
 *   <li>The LimitRecords filter orders the input in ascending order using specified record-type,
 *       before limiting the it to producing the output.
 *   <li>The records in the output may not be in ascending order.
 *   <li>This filter only supports the following record-types: market, outcome
 *   <li>The ordering of market records is based these prioritised fields: market.displayOrder,
 *       market.id.
 *   <li>The ordering of outcome records is based the current live-price record,
 *       outcome.displayOrder, outcome.id.
 *   <li>Specifying multiple LimitRecords filters for the same record-type is not allowed.
 *   <li>limitTo and limitRecords for the same record-type is not allowed in the same request.
 *       However if limitTo and limitRecords are applicable to different record-types it is allowed.
 *       For example, limitTo=market.id:isHighest&limitRecords=outcome:5 is valid. While
 *       limitTo=market.id:isHighest&limitRecords=market:5 is not valid.
 *   <li>aggregation and limitRecords for the same record-type is not allowed in the same request.
 *       For example, count=event:market&limitRecords=market:5 is not valid.
 * </ul>
 */
public class LimitRecordsFilter implements BaseFilter {

  private final List<String> queryMap;

  private LimitRecordsFilter(LimitRecordsFilter.LimitRecordsFilterBuilder builder) {
    this.queryMap = builder.queryMap;
  }

  public static class LimitRecordsFilterBuilder {
    private final List<String> queryMap = new ArrayList<>();

    public LimitRecordsFilter build() {
      return new LimitRecordsFilter(this);
    }

    public LimitRecordsFilter.LimitRecordsFilterBuilder addField(String field, int value) {
      queryMap.add(field + SEPARATOR + value);
      return this;
    }
  }

  @Override
  public List<String> getQueryMap() {
    return queryMap;
  }
}
