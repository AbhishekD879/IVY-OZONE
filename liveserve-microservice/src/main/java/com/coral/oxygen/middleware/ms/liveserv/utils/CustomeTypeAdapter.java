package com.coral.oxygen.middleware.ms.liveserv.utils;

import com.google.gson.TypeAdapter;
import com.google.gson.stream.JsonReader;
import com.google.gson.stream.JsonWriter;
import java.io.IOException;

/*
 * Implemented to handle read write operations for Json
 * For the fields which are not supported for serialization and deserialization
 * */
public class CustomeTypeAdapter extends TypeAdapter<Error> {
  private static String messageType = "message";

  @Override
  public void write(JsonWriter out, Error value) throws IOException {
    // Implementation not required in deserialization
  }

  @Override
  public Error read(JsonReader jsonReader) throws IOException {
    jsonReader.beginObject();
    String message = null;
    while (jsonReader.hasNext()) {
      String name = jsonReader.nextName();
      if (messageType.equals(name)) {
        message = jsonReader.nextString();
      } else {
        jsonReader.skipValue();
      }
    }
    jsonReader.endObject();
    return new Error(message);
  }
}
