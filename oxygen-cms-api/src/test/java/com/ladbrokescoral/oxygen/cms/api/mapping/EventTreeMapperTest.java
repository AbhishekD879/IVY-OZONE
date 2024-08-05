package com.ladbrokescoral.oxygen.cms.api.mapping;

import static org.junit.Assert.assertTrue;

import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.google.common.collect.Maps;
import com.ladbrokescoral.oxygen.cms.api.dto.SiteServeEventTreeNodeDto;
import com.ladbrokescoral.oxygen.cms.api.entity.StreamAndBetShortNode;
import java.io.IOException;
import java.io.InputStream;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.stream.Collectors;
import org.junit.Assert;
import org.junit.BeforeClass;
import org.junit.Test;

public class EventTreeMapperTest {

  private EventTreeMapper mapper = new EventTreeMapper();
  private static List<SiteServeEventTreeNodeDto> nodeList;
  private static Map<String, LinkedHashSet<StreamAndBetShortNode>> expected;

  @BeforeClass
  public static void setup() throws IOException {
    ObjectMapper objectMapper = new ObjectMapper();

    InputStream nodelistis = EventTreeMapperTest.class.getResourceAsStream("nodeList.json");
    InputStream expectedis = EventTreeMapperTest.class.getResourceAsStream("nodeToMapResult.json");

    nodeList =
        objectMapper.readValue(nodelistis, new TypeReference<List<SiteServeEventTreeNodeDto>>() {});
    expected =
        objectMapper.readValue(
            expectedis, new TypeReference<Map<String, LinkedHashSet<StreamAndBetShortNode>>>() {});
  }

  @Test
  public void toDtoMapTest() {

    Map<String, Set<StreamAndBetShortNode>> result = mapper.toDtoMap(nodeList);
    assertTrue(Maps.difference(expected, result).areEqual());
  }

  @Test
  public void toDtoMapSortedTest() {
    Map<String, Set<StreamAndBetShortNode>> result = mapper.toDtoMap(nodeList);
    List<String> resultNodes =
        result.get("97").stream().map(StreamAndBetShortNode::getName).collect(Collectors.toList());
    List<String> expectedNodes =
        expected.get("97").stream()
            .map(StreamAndBetShortNode::getName)
            .collect(Collectors.toList());

    Assert.assertEquals(expectedNodes, resultNodes);
  }
}
