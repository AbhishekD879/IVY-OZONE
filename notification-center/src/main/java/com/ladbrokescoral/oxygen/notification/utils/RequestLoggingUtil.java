package com.ladbrokescoral.oxygen.notification.utils;

import java.io.IOException;
import java.io.InputStream;
import java.io.StringWriter;
import javax.servlet.http.HttpServletRequest;
import org.apache.commons.io.IOUtils;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.web.util.ContentCachingRequestWrapper;
import org.springframework.web.util.WebUtils;

public class RequestLoggingUtil {

  private static final Logger logger = LoggerFactory.getLogger(RequestLoggingUtil.class);

  public static String getStringFromInputStream(InputStream is) {
    StringWriter writer = new StringWriter();
    String encoding = "UTF-8";
    try {
      IOUtils.copy(is, writer, encoding);
    } catch (IOException e) {
      logger.error(e.getMessage());
    }
    return writer.toString();
  }

  public static String readPayload(final HttpServletRequest request) throws IOException {
    String payloadData = null;
    ContentCachingRequestWrapper contentCachingRequestWrapper =
        WebUtils.getNativeRequest(request, ContentCachingRequestWrapper.class);
    if (null != contentCachingRequestWrapper) {
      byte[] buf = contentCachingRequestWrapper.getContentAsByteArray();
      if (buf.length > 0) {
        payloadData =
            new String(buf, 0, buf.length, contentCachingRequestWrapper.getCharacterEncoding());
      }
    }
    return payloadData;
  }
}
