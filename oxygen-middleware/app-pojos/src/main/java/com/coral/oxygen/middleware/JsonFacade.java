package com.coral.oxygen.middleware;

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import com.google.gson.JsonDeserializationContext;
import com.google.gson.JsonDeserializer;
import com.google.gson.JsonElement;
import java.lang.reflect.Type;
import java.util.function.Consumer;
import lombok.AccessLevel;
import lombok.NoArgsConstructor;
import org.joda.time.DateTime;

@NoArgsConstructor(access = AccessLevel.PRIVATE)
public class JsonFacade {

  public static final Gson GSON;

  public static final GsonBuilder GSON_BUILDER;

  public static final Gson PRETTY_GSON;

  public static final Gson NO_ESCAPING_GSON;

  static {
    GSON_BUILDER = new GsonBuilder();
    JsonDeserializer<DateTime> jsonDeserializer =
        (JsonElement json, Type typeOfT, JsonDeserializationContext context) ->
            new DateTime(json.getAsJsonPrimitive().getAsString());
    GSON_BUILDER.registerTypeAdapter(DateTime.class, jsonDeserializer);

    GSON = GSON_BUILDER.create();
    PRETTY_GSON = GSON_BUILDER.setPrettyPrinting().create();
    NO_ESCAPING_GSON = GSON_BUILDER.disableHtmlEscaping().create();
  }

  public static Gson createParser(Consumer<GsonBuilder> injector) {
    injector.accept(GSON_BUILDER);
    return GSON_BUILDER.create();
  }
}
