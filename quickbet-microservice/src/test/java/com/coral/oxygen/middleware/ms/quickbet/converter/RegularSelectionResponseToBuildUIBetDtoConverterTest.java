package com.coral.oxygen.middleware.ms.quickbet.converter;

import static org.assertj.core.api.Assertions.assertThat;

import com.coral.oxygen.middleware.ms.quickbet.connector.dto.response.v2.RegularSelectionResponse;
import com.coral.oxygen.middleware.ms.quickbet.utils.TestUtils;
import com.entain.oxygen.bettingapi.model.bet.api.request.BuildBetsDto;
import java.util.Arrays;
import java.util.Collection;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.MethodSource;

class RegularSelectionResponseToBuildUIBetDtoConverterTest {

  static Collection getParams() {
    return Arrays.asList(
        new Object[][] {
          {
            "testConvertWithEachWay",
            "converter/regularSelectionResponseToBuildBetDtoConverter/selectionResponse_with_each_way.json",
            "converter/regularSelectionResponseToBuildBetDtoConverter/buildBetReq_with_each_way.json"
          },
          {
            "testConvertWithoutEachWay",
            "converter/regularSelectionResponseToBuildBetDtoConverter/selectionResponse.json",
            "converter/regularSelectionResponseToBuildBetDtoConverter/buildBetReq.json"
          }
        });
  }

  @ParameterizedTest(name = "{0}")
  @MethodSource("getParams")
  void testConvert(String testName, String responsePath, String betBuildReqPath) {
    RegularSelectionResponse response =
        TestUtils.deserializeWithGson(responsePath, RegularSelectionResponse.class);
    String buildBetsDto = TestUtils.getResourceByPath(betBuildReqPath);
    buildBetsDto = buildBetsDto.trim();

    RegularSelectionResponseToBuildBetDtoConverter converter =
        new RegularSelectionResponseToBuildBetDtoConverter();

    BuildBetsDto actual = converter.convert(response);
    assertThat(TestUtils.GSON.toJson(actual)).isEqualTo(buildBetsDto);
  }
}
