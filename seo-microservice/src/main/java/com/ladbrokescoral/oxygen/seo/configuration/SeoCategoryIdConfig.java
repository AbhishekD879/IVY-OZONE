package com.ladbrokescoral.oxygen.seo.configuration;

import java.util.HashMap;
import java.util.Map;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class SeoCategoryIdConfig {

  @Bean
  public Map<String, String> categoryIdConfigs() {
    Map<String, String> categoryIds = new HashMap<>();
    categoryIds.put("football", "16");
    categoryIds.put("horse-racing", "21");
    categoryIds.put("greyhound-racing", "19");
    categoryIds.put("golf", "18");
    categoryIds.put("cricket", "10");
    categoryIds.put("tennis", "34");
    categoryIds.put("Table Tennis", "59");
    categoryIds.put("american-football", "1");
    categoryIds.put("athletics", "2");
    categoryIds.put("aussie-rules", "3");
    categoryIds.put("badminton", "51");
    categoryIds.put("baseball", "5");
    categoryIds.put("basketball", "6");
    categoryIds.put("beach-volleyball", "52");
    categoryIds.put("bowls", "8");
    categoryIds.put("boxing", "9");
    categoryIds.put("christmas-specials", "68");
    categoryIds.put("darts", "13");
    categoryIds.put("esports", "148");
    categoryIds.put("formula-1", "24");
    categoryIds.put("handball", "20");
    categoryIds.put("ice-hockey", "22");
    categoryIds.put("motor-bikes", "23");
    categoryIds.put("motor-sports", "26");
    categoryIds.put("rugby-league", "30");
    categoryIds.put("rugby-union", "31");
    categoryIds.put("pool", "28");
    categoryIds.put("snooker", "32");
    categoryIds.put("tv-specials", "48");
    categoryIds.put("volleyball", "36");
    categoryIds.put("hockey", "54");
    categoryIds.put("chess", "132");
    categoryIds.put("cycling", "12");
    categoryIds.put("wrestling", "105");
    categoryIds.put("ufc-mma", "35");
    categoryIds.put("gaa", "154");
    return categoryIds;
  }
}
