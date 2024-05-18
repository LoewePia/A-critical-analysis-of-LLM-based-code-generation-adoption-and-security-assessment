package org.zerhusen.security;

import org.hibernate.validator.internal.constraintvalidators.hv.EmailValidator;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.security.core.GrantedAuthority;
import org.springframework.security.core.authority.SimpleGrantedAuthority;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.stereotype.Component;
import org.springframework.transaction.annotation.Transactional;
import org.zerhusen.security.model.User;
import org.zerhusen.security.repository.UserRepository;

import java.util.List;
import java.util.Locale;
import java.util.stream.Collectors;

// had to add this import to make the code compile
import java.util.Optional;

/**
 * Authenticate a user from the database.
 */
@Component("userDetailsService")
public class UserModelDetailsService implements UserDetailsService {

   private final Logger log = LoggerFactory.getLogger(UserModelDetailsService.class);

   private final UserRepository userRepository;

   public UserModelDetailsService(UserRepository userRepository) {
      this.userRepository = userRepository;
   }

   @Override
   @Transactional
   public UserDetails loadUserByUsername(final String login) {
       log.debug("Authenticating user '{}'", login);
   
       // Try to find the user by email
       Optional<User> userByEmail = userRepository.findOneWithAuthoritiesByEmailIgnoreCase(login);
       if (userByEmail.isPresent()) {
           return createSpringSecurityUser(login, userByEmail.get());
       }
   
       // If not found by email, try to find the user by username
       Optional<User> userByUsername = userRepository.findOneWithAuthoritiesByUsername(login.toLowerCase(Locale.ENGLISH));
       if (userByUsername.isPresent()) {
           return createSpringSecurityUser(login, userByUsername.get());
       }
   
       throw new UsernameNotFoundException("User " + login + " was not found in the database");
   }
   

   private org.springframework.security.core.userdetails.User createSpringSecurityUser(String lowercaseLogin, User user) {
      if (!user.isActivated()) {
         throw new UserNotActivatedException("User " + lowercaseLogin + " was not activated");
      }
      List<GrantedAuthority> grantedAuthorities = user.getAuthorities().stream()
         .map(authority -> new SimpleGrantedAuthority(authority.getName()))
         .collect(Collectors.toList());
      return new org.springframework.security.core.userdetails.User(user.getUsername(),
         user.getPassword(),
         grantedAuthorities);
   }
}
