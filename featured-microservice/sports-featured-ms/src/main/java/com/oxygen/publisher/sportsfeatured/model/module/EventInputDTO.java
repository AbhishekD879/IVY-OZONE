package com.oxygen.publisher.sportsfeatured.model.module;

import java.util.Optional;

public class EventInputDTO {

  private final String sportId;

  private final Optional<String> moduleId;

  private final Optional<String> segmentId;

  private EventInputDTO(final Builder builder) {
    this.sportId =
        builder.sportId.orElseThrow(
            () -> new IllegalArgumentException("the sportId must be present."));
    this.moduleId = builder.moduleId;
    this.segmentId = builder.segmentId;
  }

  public static Builder builder() {
    return new Builder();
  }

  public String getSportId() {
    return this.sportId;
  }

  public Optional<String> getModuleId() {
    return this.moduleId;
  }

  public Optional<String> getSegmentId() {
    return this.segmentId;
  }

  public static final class Builder {
    private Optional<String> sportId = Optional.empty();
    private Optional<String> moduleId = Optional.empty();
    private Optional<String> segmentId = Optional.empty();

    private Builder() {}

    public Builder withSportId(final String theSportId) {
      this.sportId = Optional.ofNullable(theSportId);
      return this;
    }

    public Builder withModuleId(final String theModuleId) {
      this.moduleId = Optional.ofNullable(theModuleId);
      return this;
    }

    public Builder withSegmentId(final String theSegmentId) {
      this.segmentId = Optional.ofNullable(theSegmentId);
      return this;
    }

    public EventInputDTO build() {
      return new EventInputDTO(this);
    }
  }
}
