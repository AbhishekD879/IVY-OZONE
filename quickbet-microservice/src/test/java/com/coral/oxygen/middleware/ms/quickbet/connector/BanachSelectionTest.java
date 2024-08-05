package com.coral.oxygen.middleware.ms.quickbet.connector;

import static org.assertj.core.api.Assertions.assertThat;

import com.coral.oxygen.middleware.ms.quickbet.connector.dto.request.BanachSelectionRequestData;
import com.ladbrokescoral.oxygen.byb.banach.dto.external.VirtualSelectionDto;
import java.util.Arrays;
import java.util.List;
import org.junit.jupiter.api.Test;

public class BanachSelectionTest {

  public static BanachSelectionRequestData banachSelectionRequest(
      long eventId, List<Long> selectionIds, List<VirtualSelectionDto> playerSelections) {
    BanachSelectionRequestData banachSelectionRequestData = new BanachSelectionRequestData();
    banachSelectionRequestData.setObEventId(eventId);
    if (selectionIds != null) {
      banachSelectionRequestData.setSelectionIds(selectionIds);
    }
    if (playerSelections != null) {
      banachSelectionRequestData.setPlayerSelections(playerSelections);
    }
    return banachSelectionRequestData;
  }

  @Test
  public void twoEqualSelectionsHaveTheSameHash() {
    BanachSelection b1 =
        new BanachSelection(banachSelectionRequest(123L, Arrays.asList(1L, 2L), null));

    BanachSelection b2 =
        new BanachSelection(banachSelectionRequest(123L, Arrays.asList(1L, 2L), null));

    assertThat(b2.selectionHash()).isEqualTo(b1.selectionHash());
  }

  @Test
  public void twoSelectionHaveTheSameHashDespiteOrderOfSelectionIds() {
    BanachSelection b1 =
        new BanachSelection(banachSelectionRequest(123L, Arrays.asList(1L, 2L, 3L), null));

    BanachSelection b2 =
        new BanachSelection(banachSelectionRequest(123L, Arrays.asList(1L, 3L, 2L), null));

    assertThat(b2.selectionHash()).isEqualTo(b1.selectionHash());
  }

  @Test
  public void twoPlayerSelectionsInDifferentOrderShouldBeSameHash() {
    VirtualSelectionDto v1 = virtualSelection(1L, 2L, 10L);
    VirtualSelectionDto v2 = virtualSelection(1L, 5L, 1L);
    BanachSelection b1 =
        new BanachSelection(banachSelectionRequest(123L, null, Arrays.asList(v1, v2)));
    BanachSelection b2 =
        new BanachSelection(banachSelectionRequest(123L, null, Arrays.asList(v2, v1)));

    assertThat(b2.selectionHash()).isEqualTo(b1.selectionHash());
  }

  @Test
  public void testPlayerAndTeamSelections() {
    VirtualSelectionDto v1 = virtualSelection(2L, 3L, 5L);
    VirtualSelectionDto v2 = virtualSelection(1L, 5L, 3L);
    BanachSelection b1 =
        new BanachSelection(banachSelectionRequest(123L, Arrays.asList(1L), Arrays.asList(v1, v2)));
    BanachSelection b2 =
        new BanachSelection(banachSelectionRequest(123L, Arrays.asList(1L), Arrays.asList(v2, v1)));

    assertThat(b2.selectionHash()).isEqualTo(b1.selectionHash());
  }

  public static VirtualSelectionDto virtualSelection(long playerId, long statId, long line) {
    VirtualSelectionDto virtualSelectionDto = new VirtualSelectionDto();
    virtualSelectionDto.setLine(line);
    virtualSelectionDto.setPlayerId(playerId);
    virtualSelectionDto.setStatId(statId);
    return virtualSelectionDto;
  }
}
