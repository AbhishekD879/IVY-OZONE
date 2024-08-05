package com.coral.oxygen.middleware.featured.utils

import com.coral.oxygen.middleware.pojos.model.output.EventsModuleData
import com.coral.oxygen.middleware.pojos.model.output.OutputMarket
import com.coral.oxygen.middleware.pojos.model.output.OutputOutcome
import com.coral.oxygen.middleware.pojos.model.output.OutputPrice
import com.egalacoral.spark.siteserver.model.Event
import com.egalacoral.spark.siteserver.model.Market
import com.egalacoral.spark.siteserver.model.Outcome
import com.egalacoral.spark.siteserver.model.Price
import com.egalacoral.spark.siteserver.model.RacingFormOutcome

class DataToOutputData {
  static verifyOutcome(OutputOutcome o, Outcome outcome){
    assert o.getName() == outcome.getName()
    assert o.getOutcomeMeaningMajorCode() == outcome.getOutcomeMeaningMajorCode()
    assert o.getOutcomeMeaningMinorCode() == outcome.getOutcomeMeaningMinorCode()
    assert o.getOutcomeMeaningScores() == outcome.getOutcomeMeaningScores()
    assert o.getRunnerNumber() == outcome.getRunnerNumber()
    assert o.getResulted() == outcome.getIsResulted()
    assert o.getOutcomeStatusCode() == outcome.getOutcomeStatusCode()
    assert o.getLiveServChannels() == outcome.getLiveServChannels()
    assert (o.getCorrectPriceType() == null || o.getCorrectPriceType() == "SP" || o.getCorrectPriceType() == "LP")
    assert Arrays.asList(null, 1, 2, 3).contains(o.getCorrectedOutcomeMeaningMinorCode())

    return true
  }

  static verifyPrice(OutputPrice p, Price price) {
    assert p.getPriceType() == price.getPriceType()
    assert p.getPriceNum() == price.getPriceNum()
    assert p.getPriceDec() == price.getPriceDec()
    assert p.getPriceDen() == price.getPriceDen()
    assert p.getHandicapValueDec() == price.getHandicapValueDec()
    assert p.getRawHandicapValue() == price.getRawHandicapValue()

    return true
  }

  static verifyRacingFormOutcome(OutputOutcome o, RacingFormOutcome racingFormOutcome){
    assert o.getRacingFormOutcome() != null
    assert o.getRacingFormOutcome().getId() == racingFormOutcome.getId()
    assert o.getRacingFormOutcome().getRefRecordId() == racingFormOutcome.getRefRecordId()
    assert o.getRacingFormOutcome().getRunnerNumber() == racingFormOutcome.getRunnerNumber()
    assert o.getRacingFormOutcome().getRunnerId() == racingFormOutcome.getRunnerId()
    assert o.getRacingFormOutcome().getAge() == racingFormOutcome.getAge()
    assert o.getRacingFormOutcome().getTrainer() == racingFormOutcome.getTrainer()
    assert o.getRacingFormOutcome().getDaysSinceRun() == racingFormOutcome.getDaysSinceRun()
    assert o.getRacingFormOutcome().getDraw() == racingFormOutcome.getDraw()
    assert o.getRacingFormOutcome().getJockey() == racingFormOutcome.getJockey()
    assert o.getRacingFormOutcome().getOwner() == racingFormOutcome.getOwner()
    assert o.getRacingFormOutcome().getSilkName() == racingFormOutcome.getSilkName()
    assert o.getRacingFormOutcome().getFormGuide() == racingFormOutcome.getFormGuide()
    assert o.getRacingFormOutcome().getOverview() == racingFormOutcome.getOverview()
    assert o.getRacingFormOutcome().getSireOverview() == racingFormOutcome.getSireOverview()
    assert o.getRacingFormOutcome().getBreedingOverview() == racingFormOutcome.getBreedingOverview()
    assert o.getRacingFormOutcome().getWeight() == racingFormOutcome.getWeight()
    assert o.getRacingFormOutcome().getOfficialRating() == racingFormOutcome.getOfficialRating()
    assert o.getRacingFormOutcome().getFormProviderRating() == racingFormOutcome.getFormProviderRating()
    assert o.getRacingFormOutcome().getRunnerStatusCode() == racingFormOutcome.getRunnerStatusCode()
    assert o.getRacingFormOutcome().getColour() == racingFormOutcome.getColour()
    assert o.getRacingFormOutcome().getGenderCode() == racingFormOutcome.getGenderCode()

    return true
  }

  static verifyMarket(OutputMarket m, Market market) {
    assert m.getId() == market.getId()
    assert m.getName() == market.getName()
    assert m.getLpAvailable() == market.getIsLpAvailable()
    assert m.getSpAvailable() == market.getIsSpAvailable()
    assert m.getGpAvailable() == market.getIsGpAvailable()
    assert m.getEachWayFactorNum() == market.getEachWayFactorNum()
    assert m.getEachWayFactorDen() == market.getEachWayFactorDen()
    assert m.getEachWayPlaces() == market.getEachWayPlaces()
    assert m.getPriceTypeCodes() != null
    assert m.getNcastTypeCodes() == market.getNcastTypeCodes()
    assert m.getCashoutAvail() == market.getCashoutAvail()
    assert m.getMarketMeaningMajorCode() == market.getMarketMeaningMajorCode()
    assert m.getMarketMeaningMinorCode() == market.getMarketMeaningMinorCode()
    assert m.getMarketBetInRun() == market.getIsMarketBetInRun()
    assert (m.getTerms() == null || m.getTerms().startsWith("Each Way: "))
    assert (m.getHandicapType() == null || m.getHandicapType() == "matchResult" || m.getHandicapType() == "firstHalf" || m.getHandicapType() == "secondHalf")
    assert (m.getViewType() == "handicaps" || m.getViewType() == "correctScore" || m.getViewType().startsWith("columns-"))

    return true
  }

  static verifyDataItemEmpty(EventsModuleData item) {
    assert item.getNameOverride() != null
    assert item.getEventSortCode() == null
    assert item.getStartTime() == null
    assert item.getLiveServChannels() == null
    assert item.getLiveServChildrenChannels() == null
    assert item.getLiveServLastMsgId() == null
    assert item.getCategoryId() == null
    assert item.getCategoryCode() == null
    assert item.getCategoryName() == null
    assert item.getTypeName() == null
    assert item.getCashoutAvail() == null
    assert item.getDisplayOrder() == null
    assert item.getStarted() == null
    assert item.getFinished() == null
    assert item.getResponseCreationTime() == null
    assert item.getMarkets() != null
    assert item.getMarkets().size() == 0


    return true
  }

  static verifyDataItem(EventsModuleData item, Event event) {
    assert item.getEventSortCode() == event.getEventSortCode()
    assert item.getStartTime() == event.getStartTime()
    assert item.getLiveServChannels() == event.getLiveServChannels()
    assert item.getLiveServChildrenChannels() == event.getLiveServChildrenChannels()
    assert item.getLiveServLastMsgId() == event.getLiveServLastMsgId()
    assert item.getCategoryId() == event.getCategoryId()
    assert item.getCategoryCode() == event.getCategoryCode()
    assert item.getCategoryName() == event.getCategoryName()
    assert item.getTypeName() == event.getTypeName()
    assert item.getCashoutAvail() == event.getCashoutAvail()
    assert item.getDisplayOrder() == event.getDisplayOrder()
    assert item.getStarted() == event.getIsStarted()
    assert item.getFinished() == event.getIsFinished()
    assert item.getResponseCreationTime() == event.getResponseCreationTime()
    assert item.getMarkets() != null
    assert (item.isLiveStreamAvailable() == true || item.isLiveStreamAvailable() == false)
    assert (item.getUS() == true || item.getUS() == false)
    assert (item.getEventIsLive() == true || item.getEventIsLive() == false)

    return true
  }
}
