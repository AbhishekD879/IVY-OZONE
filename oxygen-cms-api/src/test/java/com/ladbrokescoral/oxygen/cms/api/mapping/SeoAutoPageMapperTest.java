package com.ladbrokescoral.oxygen.cms.api.mapping;

import static org.junit.Assert.assertTrue;

import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.google.common.collect.Maps;
import com.ladbrokescoral.oxygen.cms.api.dto.SeoAutoInitDataDto;
import com.ladbrokescoral.oxygen.cms.api.entity.SeoAutoPage;
import java.io.IOException;
import java.io.InputStream;
import java.util.List;
import java.util.Map;
import org.junit.BeforeClass;
import org.junit.Test;

public class SeoAutoPageMapperTest {

  private SeoAutoPageMapper mapper;
  private static List<SeoAutoPage> nodeList;
  private static Map<String, SeoAutoInitDataDto> expected;

  @BeforeClass
  public static void setup() throws IOException {
    ObjectMapper objectMapper = new ObjectMapper();

    InputStream nodelistis = SeoAutoPageMapperTest.class.getResourceAsStream("SeoAutoPages.json");
    InputStream expectedis =
        SeoAutoPageMapperTest.class.getResourceAsStream("SeoAutoPageJsonResult.json");

    nodeList = objectMapper.readValue(nodelistis, new TypeReference<List<SeoAutoPage>>() {});
    expected =
        objectMapper.readValue(expectedis, new TypeReference<Map<String, SeoAutoInitDataDto>>() {});
  }

  @Test
  public void toDtoMapTest() {

    Map<String, SeoAutoInitDataDto> result = SeoAutoPageMapper.toDto(nodeList);
    assertTrue(Maps.difference(expected, result).areEqual());
  }
}
