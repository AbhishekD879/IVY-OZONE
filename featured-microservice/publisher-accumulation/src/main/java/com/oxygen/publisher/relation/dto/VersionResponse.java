package com.oxygen.publisher.relation.dto;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * A response DTO that holds the Middleware Service model version.
 *
 * @author tvuyiv
 */
@Data
@AllArgsConstructor
@NoArgsConstructor
public class VersionResponse {

  private String value;
}
