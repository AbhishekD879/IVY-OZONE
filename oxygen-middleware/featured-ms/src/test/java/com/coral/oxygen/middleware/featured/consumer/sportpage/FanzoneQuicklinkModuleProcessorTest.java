package com.coral.oxygen.middleware.featured.consumer.sportpage;

import com.coral.oxygen.middleware.pojos.model.output.featured.FanzoneSegmentView;
import com.coral.oxygen.middleware.pojos.model.output.featured.QuickLinkData;
import com.coral.oxygen.middleware.pojos.model.output.featured.QuickLinkModule;
import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;
import org.junit.Assert;
import org.junit.Test;

public class FanzoneQuicklinkModuleProcessorTest {
  @Test
  public void testProcessFanzoneSegmentwiseModules() {
    FanzoneQuickLinkModuleProcessor moduleProcessor = new FanzoneQuickLinkModuleProcessor();
    QuickLinkData quickLinkData = new QuickLinkData();
    quickLinkData.setId("12345");
    quickLinkData.setFanzoneSegments(Arrays.asList("1234"));
    QuickLinkModule module = new QuickLinkModule();
    module.setData(Arrays.asList(quickLinkData));
    FanzoneSegmentView fanzoneSegmentView = new FanzoneSegmentView();
    Map<String, QuickLinkData> fzMap = new HashMap<>();
    fanzoneSegmentView.setQuickLinkModuleData(fzMap);
    Map<String, FanzoneSegmentView> segmentWiseMap = new HashMap<>();
    segmentWiseMap.put("1", fanzoneSegmentView);
    moduleProcessor.processFanzoneSegmentwiseModules(module, segmentWiseMap);
    Assert.assertEquals(2, segmentWiseMap.size());
  }

  @Test
  public void testProcessFanzoneSegmentwiseModulesWithMatchedData() {
    FanzoneQuickLinkModuleProcessor moduleProcessor = new FanzoneQuickLinkModuleProcessor();
    QuickLinkData quickLinkData = new QuickLinkData();
    quickLinkData.setId("123");
    quickLinkData.setFanzoneSegments(Arrays.asList("123"));
    QuickLinkModule module = new QuickLinkModule();
    module.setData(Arrays.asList(quickLinkData));
    FanzoneSegmentView fanzoneSegmentView = new FanzoneSegmentView();
    Map<String, QuickLinkData> fzMap = new HashMap<>();
    fanzoneSegmentView.setQuickLinkModuleData(fzMap);
    Map<String, FanzoneSegmentView> segmentWiseMap = new HashMap<>();
    segmentWiseMap.put("123", fanzoneSegmentView);
    module.setFanzoneModuleSegmentView(segmentWiseMap);
    moduleProcessor.processFanzoneSegmentwiseModules(module, segmentWiseMap);
    Assert.assertEquals(1, segmentWiseMap.size());
  }
}
