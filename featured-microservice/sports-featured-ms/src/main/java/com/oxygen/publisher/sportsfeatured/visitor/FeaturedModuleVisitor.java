package com.oxygen.publisher.sportsfeatured.visitor;

import com.oxygen.publisher.sportsfeatured.model.module.*;

public interface FeaturedModuleVisitor {
  void visit(QuickLinkModule module);

  void visit(RecentlyPlayedGameModule module);

  void visit(EventsModule module);

  void visit(HighlightCarouselModule module);

  void visit(VirtualEventModule module);

  void visit(PopularBetModule module);

  void visit(InplayModule module);

  void visit(SurfaceBetModule module);

  void visit(AemBannersModule module);

  void visit(RacingModule module);

  void visit(RacingEventsModule module);

  void visit(VirtualRaceModule module);

  void visit(InternationalToteRaceModule module);

  void visit(QuickLinkModule module, String segment);

  void visit(BybWidgetModule module);

  void visit(SurfaceBetModule module, String segment);

  void visit(InplayModule module, String segment);

  void visit(TeamBetsModule module);

  void visit(FanBetsModule module);

  void visit(FanBetsModule module, String segment);

  void visit(TeamBetsModule module, String segment);

  void visit(LuckyDipModule module);

  void visit(SuperButtonModule superButtonModule);

  void visit(PopularAccaModule module);
}
