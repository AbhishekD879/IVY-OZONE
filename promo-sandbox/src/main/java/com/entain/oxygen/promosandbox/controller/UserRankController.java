package com.entain.oxygen.promosandbox.controller;

import com.entain.oxygen.promosandbox.dto.UserRankRequestDto;
import com.entain.oxygen.promosandbox.dto.UserRankResponseDto;
import com.entain.oxygen.promosandbox.service.UserRankService;
import javax.validation.Valid;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

@RestController
@Slf4j
public class UserRankController implements AbstractApi {

  private final UserRankService userRankService;

  @Autowired
  public UserRankController(UserRankService userRankService) {
    this.userRankService = userRankService;
  }

  @PostMapping(value = "user-rank")
  public UserRankResponseDto fetchUserRankDetails(
      @RequestHeader(value = "token", required = false) String token,
      @RequestBody @Valid UserRankRequestDto requestDto) {
    log.info("userRank API request:{} ", requestDto);
    return userRankService.fetchUserRankDetails(requestDto, token);
  }
}
