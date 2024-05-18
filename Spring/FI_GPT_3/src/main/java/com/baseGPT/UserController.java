package com.baseGPT;

import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api")
public class UserController {
    
    @PostMapping("/authenticate")
    public ResponseEntity<?> createAuthenticationToken(@RequestBody AuthenticationRequest authenticationRequest) throws Exception {
        // Authenticate the user
        // Generate JWT token
        final String token = jwtTokenUtil.generateToken(authenticationRequest.getUsername());
        return ResponseEntity.ok(new AuthenticationResponse(token));
    }
    
    @GetMapping("/hello")
    public String hello() {
        return "Hello, World!";
    }
    
    // Other endpoints...
}

