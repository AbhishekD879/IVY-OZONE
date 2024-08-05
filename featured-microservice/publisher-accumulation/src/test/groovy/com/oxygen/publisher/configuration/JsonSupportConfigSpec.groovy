package com.oxygen.publisher.configuration

import com.fasterxml.jackson.databind.ObjectMapper
import com.oxygen.publisher.model.BaseObject
import spock.lang.Specification

class JsonSupportConfigSpec extends Specification {

  ObjectMapper objectMapper = new JsonSupportConfig().objectMapper()
  static final String TEST_PRICE = "{\"publishedDate\":\"Jan 22, 2018 4:06:03 PM\",\"type\":\"PRICE\",\"event\":{\"eventId\":6962860,\"market\":{\"outcome\":{\"outcomeId\":466808177,\"hasPriceStream\":true,\"price\":{\"status\":\"Active\",\"lp_den\":\"5\",\"lp_num\":\"1\",\"ps_den\":\"5\",\"ps_num\":\"5\",\"stream_type\":\"priceBoost\"}}}}}"
  static final String TEST_EVENT1 = "{\"publishedDate\":\"Jan 22, 2018 4:41:53 PM\",\"type\":\"EVENT\",\"event\":{\"eventId\":7006694,\"market\":{\"outcome\":{\"hasPriceStream\":true}},\"status\":\"S\",\"displayed\":\"Y\",\"result_conf\":\"N\",\"disporder\":0,\"start_time\":\"2018-01-22 09:00:00\",\"start_time_xls\":{\"en\":\"22nd of Jan 2018  09:00 am\"},\"suspend_at\":\"\",\"is_off\":\"-\",\"started\":\"Y\",\"race_stage\":\"\"}}"
  static final String TEST_EVENT2 = "{\"publishedDate\":\"Jan 22, 2018 3:14:06 PM\",\"type\":\"EVENT\",\"event\":{\"eventId\":7779274,\"market\":{\"outcome\":{\"hasPriceStream\":true}},"+
  "\"names\":{\"en\":\"Australian Open Women's Outright 2018\"},\"status\":\"A\",\"displayed\":\"Y\",\"result_conf\":\"N\",\"disporder\":-5,\"start_time\":\"2018-01-23 01:30:00\",\"start_time_xls\":{\"en\":\"23rd of Jan 2018  01:30 am\"},\"suspend_at\":\"\",\"is_off\":\"N\",\"started\":\"N\",\"race_stage\":\"\"}}"
  static final String TEST_SELCN = "{\"publishedDate\":\"Jan 22, 2018 4:39:40 PM\",\"type\":\"SELCN\",\"event\":{\"eventId\":7006694,\"market\":{\"outcome\":{\"status\":\"S\",\"settled\":\"N\",\"result\":\"-\",\"displayed\":\"Y\",\"disporder\":0,\"runner_num\":\"\",\"fb_result\":\"H\",\"lp_num\":\"61\",\"lp_den\":\"11\",\"cs_home\":\"\",\"cs_away\":\"\",\"unique_id\":\"470114443_400a794e4582015a6613ca0a810e\",\"outcomeId\":470114443,\"hasPriceStream\":true,\"price\":{\"status\":\"Active\",\"lp_den\":\"11\",\"lp_num\":\"61\",\"ps_den\":\"5\",\"ps_num\":\"5\",\"stream_type\":\"priceBoost\"}},\"marketId\":121454527}}}"
  static final String TEST_EVMKT = "{\"publishedDate\":\"Jan 22, 2018 4:40:59 PM\",\"type\":\"EVMKT\",\"event\":{\"eventId\":7006694,\"market\":{\"outcome\":{\"hasPriceStream\":true},"+
  "\"marketId\":121454527,\"group_names\":{\"en\":\"Match Betting\"},\"ev_oc_grp_id\":\"37241\",\"mkt_disp_code\":\"MR\",\"mkt_disp_layout_columns\":\"3\",\"mkt_disp_layout_order\":\"FBRESULT\",\"mkt_type\":\"-\",\"mkt_sort\":\"MR\",\"mkt_grp_flags\":\"\",\"ev_id\":7006694,\"status\":\"S\",\"displayed\":\"Y\",\"disporder\":-500,\"bir_index\":\"\",\"raw_hcap\":\"\",\"hcap_values\":{},\"ew_avail\":\"N\",\"ew_places\":\"\",\"ew_fac_num\":\"\",\"ew_fac_den\":\"\",\"bet_in_run\":\"Y\",\"lp_avail\":\"Y\",\"sp_avail\":\"N\",\"mm_coll_id\":\"1297\",\"suspend_at\":\"\",\"collections\":[{\"collection_id\":\"619\"},{\"collection_id\":\"9507\"},{\"collection_id\":\"4920\"}]}}}"

  def priceTest() {
    String message = TEST_PRICE
    when:
    BaseObject baseObject = objectMapper.readValue(message, BaseObject.class)
    String backToJson = objectMapper.writeValueAsString(baseObject)
    then:
    baseObject != null
    backToJson == message
  }

  def testEvent2() {
    String message = TEST_EVENT2
    when:
    BaseObject baseObject = objectMapper.readValue(message, BaseObject.class)
    String backToJson = objectMapper.writeValueAsString(baseObject)
    then:
    baseObject != null
    backToJson == message
  }

  def testSELCN() {
    String message = TEST_SELCN
    when:
    BaseObject baseObject = objectMapper.readValue(message, BaseObject.class)
    String backToJson = objectMapper.writeValueAsString(baseObject)
    then:
    baseObject != null
    backToJson == message
  }

  def testEVMKT() {
    String message = TEST_EVMKT
    when:
    BaseObject baseObject = objectMapper.readValue(message, BaseObject.class)
    String backToJson = objectMapper.writeValueAsString(baseObject)
    then:
    baseObject != null
    backToJson == message
  }

  def testEvent1() {
    String message = TEST_EVENT1
    when:
    BaseObject baseObject = objectMapper.readValue(message, BaseObject.class)
    String backToJson = objectMapper.writeValueAsString(baseObject)
    then:
    baseObject != null
    backToJson == message
  }
}
