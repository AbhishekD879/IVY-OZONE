package com.coral.oxygen.middleware.ms.quickbet.impl;

import static org.assertj.core.api.Assertions.assertThat;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.when;

import com.coral.oxygen.middleware.ms.quickbet.Session;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.ComplexSelection;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.response.OutputPrice;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.response.v2.RegularSelectionResponse;
import com.entain.oxygen.bettingapi.model.bet.api.request.buildBet.BetBuildDto;
import com.entain.oxygen.bettingapi.model.bet.api.request.buildBet.OutcomeGroup;
import com.entain.oxygen.bettingapi.model.bet.api.request.buildBet.Part;
import com.entain.oxygen.bettingapi.model.bet.api.response.ErrorBody;
import com.entain.oxygen.bettingapi.model.bet.api.response.GeneralResponse;
import com.entain.oxygen.bettingapi.model.bet.api.response.buildBet.BetBuildResponseModel;
import com.entain.oxygen.bettingapi.service.BettingService;
import io.vavr.collection.List;
import java.util.function.Consumer;
import org.junit.jupiter.api.Test;
import org.mockito.Mockito;

class BuildBetOperationsTest {

  private BettingService bettingService = mock(BettingService.class);
  private SiteServerService siteServerService = mock(SiteServerService.class);
  private BuildBetOperations buildBetOperations =
      new BuildBetOperations(bettingService, siteServerService);

  @Test
  void shouldCreateBetBuildDtoWithManySimpleAndComplexSelections() {
    // given
    Session session = mockSession();
    List<String> simpleSelections = List.of("001", "002", "003");
    List<ComplexSelection> complexSelections =
        List.of(
            new ComplexSelection(ComplexSelection.Type.STRAIGHT_FORECAST, List.of("101", "102")),
            new ComplexSelection(
                ComplexSelection.Type.COMBINATION_TRICAST, List.of("201", "202", "203", "204")));

    // when
    BetBuildDto dto =
        buildBetOperations.createBetBuildDto(session, simpleSelections, complexSelections);

    // then
    assertThat(dto.getOutcomeGroup()).hasSize(4);
    assertThat(dto.getOutcomeGroup()).anySatisfy(hasBetNoAndContainsOutcomes("1", "001"));
    assertThat(dto.getOutcomeGroup()).anySatisfy(hasBetNoAndContainsOutcomes("2", "002"));
    assertThat(dto.getOutcomeGroup()).anySatisfy(hasBetNoAndContainsOutcomes("3", "003"));
    assertThat(dto.getOutcomeGroup())
        .anySatisfy(hasBetNoAndContainsOutcomes("4", "001", "002", "003"));

    assertThat(dto.getBet())
        .anySatisfy(
            bet -> {
              assertThat(bet.getBetNo()).isEqualTo("5");
              assertThat(bet.getLeg()).hasSize(1);
              assertThat(bet.getLeg())
                  .anySatisfy(
                      leg -> {
                        assertThat(leg.getLegNo()).isEqualTo("1");
                        assertThat(leg.getLegSort()).isEqualTo("SF");
                        assertThat(leg.getPart()).hasSize(2);
                        assertThat(leg.getPart())
                            .extracting(Part::getOutcome)
                            .containsExactly("101", "102");
                      });
            });
    assertThat(dto.getBet())
        .anySatisfy(
            bet -> {
              assertThat(bet.getBetNo()).isEqualTo("6");
              assertThat(bet.getLeg()).hasSize(1);
              assertThat(bet.getLeg())
                  .anySatisfy(
                      leg -> {
                        assertThat(leg.getLegNo()).isEqualTo("1");
                        assertThat(leg.getLegSort()).isEqualTo("CT");
                        assertThat(leg.getPart()).hasSize(4);
                        assertThat(leg.getPart())
                            .extracting(Part::getOutcome)
                            .containsExactly("201", "202", "203", "204");
                      });
            });
  }

  @Test
  void testCreateBuildDto() {
    Session session = mock(Session.class);
    RegularSelectionResponse regularSelectionResponse = new RegularSelectionResponse();
    OutputPrice outputPrice = new OutputPrice();
    outputPrice.setPriceStreamType("Price_boost");
    regularSelectionResponse.setSelectionPrice(outputPrice);
    List<String> simpleSelections = List.of("001", "002", "003");
    List<ComplexSelection> complexSelections =
        List.of(
            new ComplexSelection(ComplexSelection.Type.STRAIGHT_FORECAST, List.of("101", "102")),
            new ComplexSelection(
                ComplexSelection.Type.COMBINATION_TRICAST, List.of("201", "202", "203", "204")));
    when(session.getRegularSelectionResponse()).thenReturn(regularSelectionResponse);
    BetBuildDto dto =
        buildBetOperations.createBetBuildDto(session, simpleSelections, complexSelections);
    assertEquals("M", dto.getChannel());
  }

  @Test
  void testBuildBet() {
    Session session = mock(Session.class);
    RegularSelectionResponse regularSelectionResponse = new RegularSelectionResponse();
    OutputPrice outputPrice = new OutputPrice();
    outputPrice.setPriceStreamType("Price_boost");
    regularSelectionResponse.setSelectionPrice(outputPrice);
    List<String> simpleSelections = List.of("001", "002", "003");
    List<ComplexSelection> complexSelections =
        List.of(
            new ComplexSelection(ComplexSelection.Type.STRAIGHT_FORECAST, List.of("101", "102")),
            new ComplexSelection(
                ComplexSelection.Type.COMBINATION_TRICAST, List.of("201", "202", "203", "204")));
    when(session.getRegularSelectionResponse()).thenReturn(regularSelectionResponse);
    when(session.getComplexSelections()).thenReturn(complexSelections);
    when(session.getSelectedOutcomeIds()).thenReturn(simpleSelections);
    GeneralResponse<BetBuildResponseModel> bettingResponse =
        new GeneralResponse<>(new BetBuildResponseModel(), new ErrorBody());
    when(bettingService.buildBetV2(Mockito.any(), Mockito.any())).thenReturn(bettingResponse);
    BetBuildResponseModel dto = buildBetOperations.buildBet(session);
    assertNotNull(dto);
  }

  private Consumer<OutcomeGroup> hasBetNoAndContainsOutcomes(String betNo, String... outcomes) {
    return g -> {
      assertThat(g.getBetNo()).isEqualTo(betNo);
    };
  }

  private Session mockSession() {
    Session session = mock(Session.class);
    RegularSelectionResponse regularSelectionResponse = new RegularSelectionResponse();
    OutputPrice outputPrice = new OutputPrice();
    outputPrice.setPriceStreamType("Price_boost");
    regularSelectionResponse.setSelectionPrice(outputPrice);
    when(session.getToken()).thenReturn("token");
    when(session.getRegularSelectionResponse()).thenReturn(regularSelectionResponse);
    return session;
  }
}
