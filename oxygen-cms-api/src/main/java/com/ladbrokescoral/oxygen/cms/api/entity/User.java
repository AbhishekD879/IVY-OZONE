package com.ladbrokescoral.oxygen.cms.api.entity;

import com.fasterxml.jackson.annotation.JsonAutoDetect;
import com.fasterxml.jackson.annotation.JsonProperty;
import java.util.Collection;
import java.util.Collections;
import javax.validation.constraints.NotBlank;
import lombok.Builder;
import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.NoArgsConstructor;
import lombok.ToString;
import lombok.experimental.SuperBuilder;
import org.hibernate.validator.constraints.Length;
import org.springframework.data.mongodb.core.index.Indexed;
import org.springframework.data.mongodb.core.mapping.Document;
import org.springframework.data.mongodb.core.mapping.Field;
import org.springframework.security.core.GrantedAuthority;
import org.springframework.security.core.userdetails.UserDetails;

// FIXME: clean up. keep Value/Getter and SuperBuilder. Set final for @NotBlank
// FIXME: UserDetails is not fully implemented for MongoDB
@JsonAutoDetect(fieldVisibility = JsonAutoDetect.Visibility.ANY)
@Document(collection = "users")
@Data
@SuperBuilder
@NoArgsConstructor
@EqualsAndHashCode(callSuper = true)
public class User extends AbstractEntity implements UserDetails {

  private static final long serialVersionUID = -8237859012682911445L;

  @JsonProperty("isAdmin")
  @Field("isAdmin")
  @Builder.Default
  private boolean admin = false;

  @NotBlank
  @Length(min = 5)
  @ToString.Exclude
  private String password;

  @Indexed(unique = true)
  @NotBlank
  private String email;

  @Builder.Default private UserStatus status = UserStatus.ACTIVE;

  private Name name;
  private String brandCode;

  @Override
  public String getUsername() {
    return this.email;
  }

  @Override
  public boolean isAccountNonExpired() {
    return true;
  }

  @Override
  public boolean isAccountNonLocked() {
    return UserStatus.ACTIVE.equals(this.status);
  }

  @Override
  public boolean isCredentialsNonExpired() {
    return true;
  }

  @Override
  public boolean isEnabled() {
    return UserStatus.ACTIVE.equals(this.status);
  }

  // FIXME: we should support roles
  // we already have needs for following roles: USER, ADMIN, ACTUATOR, SYSTEM
  @Override
  public Collection<? extends GrantedAuthority> getAuthorities() {
    return Collections.emptyList();
  }
}
