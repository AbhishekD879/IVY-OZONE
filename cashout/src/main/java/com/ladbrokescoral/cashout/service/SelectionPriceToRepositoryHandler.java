package com.ladbrokescoral.cashout.service;

import com.ladbrokescoral.cashout.model.context.SelectionPrice;
import com.ladbrokescoral.cashout.model.safbaf.Price;
import com.ladbrokescoral.cashout.model.safbaf.Selection;
import com.ladbrokescoral.cashout.repository.SelectionPriceRepository;
import com.ladbrokescoral.cashout.service.masterslave.ExecuteOnMaster;
import com.ladbrokescoral.cashout.service.updates.pubsub.UpdateMessageHandler;
import com.newrelic.api.agent.DatastoreParameters;
import com.newrelic.api.agent.NewRelic;
import com.newrelic.api.agent.Segment;
import com.newrelic.api.agent.Trace;
import lombok.RequiredArgsConstructor;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.springframework.stereotype.Component;

@Component
@RequiredArgsConstructor
public class SelectionPriceToRepositoryHandler implements UpdateMessageHandler<Selection> {
  private final SelectionPriceRepository selectionPriceRepository;
  private static final Logger ASYNC_LOGGER = LogManager.getLogger("ASYNC_JSON_FILE_APPENDER");

  @Override
  @ExecuteOnMaster
  public void handleUpdateMessage(Selection selection) {
    saveLivePricesIfPresent(selection);
  }

  private void saveLivePricesIfPresent(Selection selection) {
    selection
        .getLpPrice()
        .ifPresent(price -> savePriceAtRedis(String.valueOf(selection.getSelectionKey()), price));
  }

  @Trace(dispatcher = true, metricName = "/Redis/Save/Price")
  private void savePriceAtRedis(String selectionId, Price price) {
    Segment segment = createNewRelicSegment();

    SelectionPrice selectionPrice =
        SelectionPrice.builder()
            .priceDen(price.getDenPrice().toString())
            .priceNum(price.getNumPrice().toString())
            .outcomeId(selectionId)
            .build();

    selectionPriceRepository
        .save(selectionId, selectionPrice)
        .subscribe(
            saved -> {
              if (saved) {
                ASYNC_LOGGER.trace(
                    "Prices saved for selection - {}, prices - {}", selectionId, selectionPrice);
              } else {
                ASYNC_LOGGER.trace(
                    "Unable save prices at Redis for selection - {}, prices - {}",
                    selectionId,
                    price);
              }
            },
            error -> {
              ASYNC_LOGGER.error(
                  "Unable save prices at Redis for selection - {}, prices - {}",
                  selectionId,
                  price,
                  error);
            },
            segment::end);
  }

  private Segment createNewRelicSegment() {

    Segment storePrices = NewRelic.getAgent().getTransaction().startSegment("storePrices");

    storePrices.reportAsExternal(
        DatastoreParameters.product("Redis")
            .collection(null)
            .operation("insert")
            .noInstance()
            .databaseName("SelectionPrice")
            .build());

    return storePrices;
  }
}
