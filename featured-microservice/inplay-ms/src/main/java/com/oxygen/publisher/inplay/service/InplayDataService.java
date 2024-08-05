package com.oxygen.publisher.inplay.service;

import com.oxygen.publisher.model.*;
import java.util.List;
import java.util.function.Consumer;

public interface InplayDataService {

  void getLastGeneration(Consumer<String> onSuccess);

  void getInPlayModel(String generation, Consumer<InPlayData> onSuccess);

  void getSportsRibbon(String generation, Consumer<SportsRibbon> onSuccess);

  void getInPlayCache(String generation, Consumer<InPlayCache> onSuccess);

  void getSportSegment(String storageKey, Consumer<SportSegment> onSuccess);

  void getVirtualSport(String generation, Consumer<List<VirtualSportEvents>> onSuccess);
}
