package com.egalacoral.spark.liveserver;

import java.io.IOException;
import okhttp3.Request;
import okhttp3.Response;

public interface Call {

  Response execute(Request request) throws IOException;
}
