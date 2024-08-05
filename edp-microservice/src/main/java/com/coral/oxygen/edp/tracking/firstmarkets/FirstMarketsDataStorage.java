package com.coral.oxygen.edp.tracking.firstmarkets;

import com.coral.oxygen.edp.tracking.InMemoryDataStorage;
import com.coral.oxygen.edp.tracking.model.FirstMarketsData;
import org.springframework.stereotype.Component;

/** Created by azayats on 22.12.17. */
@Component
public class FirstMarketsDataStorage extends InMemoryDataStorage<Long, FirstMarketsData> {}
