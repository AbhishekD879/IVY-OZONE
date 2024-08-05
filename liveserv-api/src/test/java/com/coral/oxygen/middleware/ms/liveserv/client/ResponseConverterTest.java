package com.coral.oxygen.middleware.ms.liveserv.client;

import com.coral.oxygen.middleware.ms.liveserv.client.model.Message;
import java.util.List;
import org.junit.Assert;
import org.junit.Test;

public class ResponseConverterTest {

  private static final String RESPONSE =
      "MsEVENT0005196558!!!!!&36[RGsEVENT0005196558000105000105{\"names\": {\"en\": \"Burnley v QPR\"}, \"status\": \"S\", \"displayed\": \"Y\", \"result_conf\": \"N\", \"disporder\": 0, \"start_time\": \"2017-02-01 13:15:00\", \"start_time_xls\": {\"en\": \"1st of Feb 2017  1:15 pm\"}, \"suspend_at\": \"\", \"is_off\": \"Y\", \"started\": \"Y\", \"race_stage\": \"\"}";

  @Test
  public void testConvertNotNull() {
    ResponseConverter converter = new ResponseConverter();
    List<Message> messages = converter.convert(RESPONSE);
    Assert.assertNotNull(messages);
  }

  @Test
  public void testConvertMessage() {
    ResponseConverter converter = new ResponseConverter();
    List<Message> messages = converter.convert(RESPONSE);
    Assert.assertEquals(1, messages.size());
    Message message = messages.get(0);
    Assert.assertEquals(
        "{\"names\": {\"en\": \"Burnley v QPR\"}, \"status\": \"S\", \"displayed\": \"Y\", \"result_conf\": \"N\", \"disporder\": 0, \"start_time\": \"2017-02-01 13:15:00\", \"start_time_xls\": {\"en\": \"1st of Feb 2017  1:15 pm\"}, \"suspend_at\": \"\", \"is_off\": \"Y\", \"started\": \"Y\", \"race_stage\": \"\"}",
        message.getJsonData());
    Assert.assertEquals(
        "MsEVENT0005196558!!!!!&36[RGsEVENT0005196558000105000105", message.getMessageCode());
  }

  @Test
  public void testMSInMessageBody() {
    ResponseConverter converter = new ResponseConverter();
    List<Message> messages =
        converter.convert(
            "MSEVENT0005366730!!!!!&`HMPGsPRICE036710608000001e00001e{\"lp_num\": \"5\", \"lp_den\": \"2\"}MSEVENT0005366730!!!!!&`HMQGsPRICE036710592000001f00001f{\"lp_num\": \"16\", \"lp_den\": \"5\"}MSEVENT0005366730!!!!!&`HMRGsPRICE036710614800001e00001e{\"lp_num\": \"2\", \"lp_den\": \"1\"}MSEVENT0005366730!!!!!&`HMSGsPRICE036710597700001f00001f{\"lp_num\": \"70\", \"lp_den\": \"1\"}MSEVENT0005366730!!!!!&`HMTGsPRICE0367105924000020000020{\"lp_num\": \"400\", \"lp_den\": \"1\"}MSEVENT0005366730!!!!!&`HMUGsPRICE0367105958000020000020{\"lp_num\": \"200\", \"lp_den\": \"1\"}MSEVENT0005366730!!!!!&`HMVGsPRICE036710595500001e00001e{\"lp_num\": \"5\", \"lp_den\": \"2\"}MSEVENT0005366730!!!!!&`HMWGsPRICE036710609500001e00001e{\"lp_num\": \"5\", \"lp_den\": \"2\"}MSEVENT0005366730!!!!!&`HMXGsPRICE036710609300001f00001f{\"lp_num\": \"14\", \"lp_den\": \"5\"}MSEVENT0005366730!!!!!&`HMYGsPRICE036710614600001e00001e{\"lp_num\": \"5\", \"lp_den\": \"2\"}MSEVENT0005366730!!!!!&`HMZGsPRICE036710591800001f00001f{\"lp_num\": \"16\", \"lp_den\": \"5\"}MSEVENT0005366730!!!!!&`HM[GsPRICE0367105898000020000020{\"lp_num\": \"33\", \"lp_den\": \"20\"}MSEVENT0005366730!!!!!&`HM\\GsPRICE036710589700001e00001e{\"lp_num\": \"4\", \"lp_den\": \"9\"}MSEVENT0005366730!!!!!&`HM]GsPRICE036710612800001e00001e{\"lp_num\": \"5\", \"lp_den\": \"2\"}MSEVENT0005366730!!!!!&`HM^GsPRICE036710605000001e00001e{\"lp_num\": \"6\", \"lp_den\": \"4\"}MSEVENT0005366730!!!!!&`HM_GsPRICE036710604800001f00001f{\"lp_num\": \"17\", \"lp_den\": \"4\"}MSEVENT0005366730!!!!!&`HM`GsPRICE036710613100001e00001e{\"lp_num\": \"9\", \"lp_den\": \"4\"}MSEVENT0005366730!!!!!&`HMaGsPRICE036710613000001e00001e{\"lp_num\": \"4\", \"lp_den\": \"9\"}MSEVENT0005366730!!!!!&`HMbGsPRICE036710613200001f00001f{\"lp_num\": \"11\", \"lp_den\": \"1\"}MSEVENT0005366730!!!!!&`HMcGsPRICE036710590000001f00001f{\"lp_num\": \"11\", \"lp_den\": \"1\"}MSEVENT0005366730!!!!!&`HMdGsPRICE036710603500001f00001f{\"lp_num\": \"28\", \"lp_den\": \"1\"}");
    Assert.assertEquals(21, messages.size());
    Assert.assertEquals(
        "MSEVENT0005366730!!!!!&`HMPGsPRICE036710608000001e00001e{\"lp_num\": \"5\", \"lp_den\": \"2\"}",
        messages.get(0).getMessageCode() + messages.get(0).getJsonData());
    Assert.assertEquals(
        "MSEVENT0005366730!!!!!&`HMdGsPRICE036710603500001f00001f{\"lp_num\": \"28\", \"lp_den\": \"1\"}",
        messages.get(20).getMessageCode() + messages.get(20).getJsonData());
  }

  @Test
  public void testConvertNull() {
    ResponseConverter converter = new ResponseConverter();
    List<Message> messages = converter.convert(null);
    Assert.assertTrue(messages.isEmpty());
  }

  @Test
  public void testConvertEmptyString() {
    ResponseConverter converter = new ResponseConverter();
    List<Message> messages = converter.convert("");
    Assert.assertTrue(messages.isEmpty());
  }
}
