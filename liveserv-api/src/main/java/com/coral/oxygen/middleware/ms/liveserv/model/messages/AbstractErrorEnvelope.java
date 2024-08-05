package com.coral.oxygen.middleware.ms.liveserv.model.messages;

import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.HashMap;
import java.util.Map;
import java.util.Objects;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/** Created by azayats on 08.05.17. */
public class AbstractErrorEnvelope extends Envelope {

  private static final transient Logger LOGGER =
      LoggerFactory.getLogger(AbstractErrorEnvelope.class);

  private final Map<String, Object> errorTrace;

  public AbstractErrorEnvelope(EnvelopeType type, String channel, String description) {
    this(type, channel, description, null);
  }

  public AbstractErrorEnvelope(EnvelopeType type, String channel, String description, Throwable e) {
    super(type, channel, description);
    this.errorTrace = buildError(e);
  }

  private static Map<String, Object> buildError(Throwable e) {
    if (Objects.isNull(e)) {
      return null;
    }
    Map<String, Object> result = new HashMap<>();
    result.put("class", e.getClass().getName());
    result.put("message", e.getMessage());
    ByteArrayOutputStream baos = new ByteArrayOutputStream();
    PrintWriter pw = new PrintWriter(baos);
    e.printStackTrace(pw);
    pw.flush();
    try {
      baos.flush();
      result.put("trace", baos.toString());
      pw.close();
      baos.close();
    } catch (IOException e1) {
      LOGGER.warn("Unexpected exception on tools stream operation");
    }
    if (Objects.nonNull(e.getCause())) {
      result.put("cause", buildError(e.getCause()));
    }
    return result;
  }

  public Map<String, Object> getErrorTrace() {
    return errorTrace;
  }

  @Override
  public String toString() {
    final StringBuffer sb = new StringBuffer("AbstractErrorEnvelope{");
    sb.append("super=").append(super.toString());
    sb.append(", errorTrace=").append(errorTrace);
    sb.append('}');
    return sb.toString();
  }
}
