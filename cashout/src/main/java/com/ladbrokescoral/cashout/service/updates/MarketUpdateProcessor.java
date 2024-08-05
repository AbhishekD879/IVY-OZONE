package com.ladbrokescoral.cashout.service.updates;

import com.ladbrokescoral.cashout.model.context.UserRequestContextAccHistory;
import com.ladbrokescoral.cashout.model.safbaf.Market;
import com.ladbrokescoral.cashout.service.SelectionData;
import com.newrelic.api.agent.NewRelic;
import java.math.BigInteger;
import java.util.Objects;
import java.util.Set;
import org.springframework.stereotype.Service;

@Service
public class MarketUpdateProcessor extends AbstractUpdateProcessor<Market>
    implements UpdateProcessor<Market> {

  private static final String KAFKA_MESSAGES_MARKET = "/Kafka/Messages/Market";

  public MarketUpdateProcessor(SelectionDataAwareUpdateProcessor<Market> processor) {
    super(processor);
  }

  /*-
   * Call BPP betDetail in case update markets related to bet
   *
   * @param context      - User related data
   * @param marketUpdate - kafka Saf market update
   */
  @Override
  public void process(UserRequestContextAccHistory context, Market marketUpdate) {
    NewRelic.incrementCounter(KAFKA_MESSAGES_MARKET);

    BigInteger marketId = marketUpdate.getMarketKey();
    if (!isUpdateImportant(marketUpdate) || marketId == null) {
      return;
    }

    Set<SelectionData> selectionsOfMarket =
        context.getIndexedData().getSelectionDataByMarketId(marketId);

    selectionDataAwareUpdateProcessor.processUpdateWithSelectionDataInContext(
        context, marketUpdate, selectionsOfMarket);
  }

  private boolean isUpdateImportant(Market market) {
    return statusesChanged(market) || handicapChanged(market);
  }

  private boolean statusesChanged(Market market) {
    return Objects.nonNull(market.getMarketStatus());
  }

  private boolean handicapChanged(Market market) {
    return Objects.nonNull(market.getHandicapValue())
        || Objects.nonNull(market.getHandicapMakeup());
  }
}
