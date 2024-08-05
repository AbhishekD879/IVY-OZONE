package com.ladbrokescoral.oxygen.cms.api;

import com.akamai.netstorage.DefaultCredential;
import com.akamai.netstorage.NetStorage;
import com.akamai.netstorage.NetStorageException;
import java.io.IOException;
import java.io.InputStream;
import java.nio.charset.Charset;
import org.apache.commons.io.IOUtils;
import org.junit.Ignore;
import org.junit.Test;

// FIXME: rework for normal testing
public class AkamaiCacheTest {

  private String akamaiHostname = "coraliassets-nsu.akamaihd.net";
  private String akamaiKeyName = "bm-mobile-tst2";
  private String akamaiKey = "16581CF46f02W7P5D4IZ3LbEIgLLUs6j4B2dG5B3xh7YZz61AJ";

  private final NetStorage netStorage;

  public AkamaiCacheTest() {
    netStorage = new NetStorage(new DefaultCredential(akamaiHostname, akamaiKeyName, akamaiKey));
  }

  @Test
  @Ignore
  public void test() throws NetStorageException, IOException {
    // println(netStorage.dir("/328873/CORAL/bet-tst2.coral.co.uk"));
    // println(netStorage.dir("/328873/CORAL/bet-tst2.coral.co.uk/desktop"));
    // println(netStorage.dir("/328873/CORAL/bet-tst2.coral.co.uk/mobile"));
    // println(netStorage.dir("/328873/CORAL/bet-tst3.coral.co.uk/cms/api/v2/bma/offers"));
  }

  private void println(InputStream stream) throws IOException {
    String result = IOUtils.toString(stream, Charset.defaultCharset());
    System.out.println(result);
  }
}
