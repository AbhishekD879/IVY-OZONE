package com.oxygen.publisher.sportsfeatured.model;

import java.util.Set;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class SportsVersionResponse {

  private Set<PageRawIndex.GenerationKey> value;
}
