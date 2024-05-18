package com.baseGPT;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.Arrays;
import java.util.List;

@RestController
@RequestMapping("/api/users")
public class UserController {

    @GetMapping
    public ResponseEntity<List<String>> getUsers(Authentication authentication) {
        // Assuming authenticated user information is required
        String username = authentication.getName();

        // Mock data
        List<String> users = Arrays.asList("User 1", "User 2", "User 3");

        return ResponseEntity.ok(users);
    }
}
