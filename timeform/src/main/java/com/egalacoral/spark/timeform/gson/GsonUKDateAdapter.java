package com.egalacoral.spark.timeform.gson;

import com.egalacoral.spark.timeform.api.tools.Tools;
import com.google.gson.JsonDeserializationContext;
import com.google.gson.JsonDeserializer;
import com.google.gson.JsonElement;
import com.google.gson.JsonParseException;
import com.google.gson.JsonPrimitive;
import com.google.gson.JsonSerializationContext;
import com.google.gson.JsonSerializer;
import java.lang.reflect.Type;
import java.text.DateFormat;
import java.text.ParseException;
import java.util.Date;

/** Created by Igor.Domshchikov on 8/19/2016. */
public class GsonUKDateAdapter implements JsonSerializer<Date>, JsonDeserializer<Date> {

  private final DateFormat dateFormat;

  public GsonUKDateAdapter() {
    dateFormat = Tools.simpleDateFormat("yyyy-MM-dd'T'HH:mm:ssZ");
  }

  @Override
  public Date deserialize(JsonElement element, Type typeOfT, JsonDeserializationContext context)
      throws JsonParseException {
    try {
      return dateFormat.parse(element.getAsString());
    } catch (ParseException e) {
      throw new JsonParseException(e);
    }
  }

  @Override
  public JsonElement serialize(Date date, Type typeOfSrc, JsonSerializationContext context) {
    return new JsonPrimitive(dateFormat.format(date));
  }

  public DateFormat getDateFormat() {
    return dateFormat;
  }
}
