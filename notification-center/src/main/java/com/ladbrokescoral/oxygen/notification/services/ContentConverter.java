package com.ladbrokescoral.oxygen.notification.services;

import com.google.gson.Gson;
import com.google.json.JsonSanitizer;
import com.ladbrokescoral.oxygen.notification.entities.sportsbook.Selection;
import com.ladbrokescoral.oxygen.notification.entities.sportsbook.SportsBookEntity;
import com.ladbrokescoral.oxygen.notification.entities.sportsbook.SportsBookUpdate;
import java.util.Optional;
import org.springframework.stereotype.Service;
import org.springframework.util.StringUtils;

@Service
public class ContentConverter {

  private Gson gson;

  public ContentConverter(Gson gson) {
    this.gson = gson;
  }

  public Optional<SportsBookEntity> convert(String message) {
    String sanitizedMessage = JsonSanitizer.sanitize(message);
    SportsBookUpdate update = gson.fromJson(sanitizedMessage, SportsBookUpdate.class);
    if (update.getEvent() != null) {
      return Optional.of(update.getEvent());
    } else if (update.getSelection() != null) {

      Selection selection = update.getSelection();

      // getting empty selection names for some selections from KafkaListenerService
      if (StringUtils.hasText(selection.getSelectionName())) {
        selection.setSelectionNameTranslated(selection.getSelectionName().replaceAll("\\|", ""));
      }
      return Optional.of(selection);
    } else {
      return Optional.empty();
    }
  }
}
