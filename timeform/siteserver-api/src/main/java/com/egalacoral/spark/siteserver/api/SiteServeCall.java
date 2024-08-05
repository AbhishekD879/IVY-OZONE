package com.egalacoral.spark.siteserver.api;

import java.util.List;
import java.util.Optional;

public interface SiteServeCall<T, H> {

  Optional<List<T>> call(List<H> lists);
}
