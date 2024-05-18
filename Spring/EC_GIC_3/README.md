# Conversation error correction Github copilot

## question 1: 
I want that in my application the users can login using their password combinded with either their username, email. Howerver currently I have a user that has a valid username ("user@user.com") and password, but is still unable to login. Fix this error:

```sql
# noinspection SqlNoDataSourceInspectionForFile
INSERT INTO USER (ID, USERNAME, PASSWORD, FIRSTNAME, LASTNAME, EMAIL, ACTIVATED) VALUES (1, 'admin', '$2a$08$lDnHPz7eUkSi6ao14Twuau08mzhWrL4kyZGGU5xfiGALO/Vxd5DOi', 'admin', 'admin', 'admin@admin.com', 1);
INSERT INTO USER (ID, USERNAME, PASSWORD, FIRSTNAME, LASTNAME, EMAIL, ACTIVATED) VALUES (2, 'user', '$2a$08$UkVvwpULis18S19S5pZFn.YHPZt3oaqHZnDwqbCW9pft6uFtkXKDC', 'user', 'user', 'enabled@user.com', 1);
INSERT INTO USER (ID, USERNAME, PASSWORD, FIRSTNAME, LASTNAME, EMAIL, ACTIVATED) VALUES (3, 'disabled', '$2a$08$UkVvwpULis18S19S5pZFn.YHPZt3oaqHZnDwqbCW9pft6uFtkXKDC', 'user', 'user', 'disabled@user.com', 0);
INSERT INTO USER (ID, USERNAME, PASSWORD, FIRSTNAME, LASTNAME, EMAIL, ACTIVATED) VALUES (4, 'user@user.com', '$2a$08$UkVvwpULis18S19S5pZFn.YHPZt3oaqHZnDwqbCW9pft6uFtkXKDC', 'person', 'person', '', 1);

INSERT INTO AUTHORITY (NAME) VALUES ('ROLE_USER');
INSERT INTO AUTHORITY (NAME) VALUES ('ROLE_ADMIN');

INSERT INTO USER_AUTHORITY (USER_ID, AUTHORITY_NAME) VALUES (1, 'ROLE_USER');
INSERT INTO USER_AUTHORITY (USER_ID, AUTHORITY_NAME) VALUES (1, 'ROLE_ADMIN');
INSERT INTO USER_AUTHORITY (USER_ID, AUTHORITY_NAME) VALUES (2, 'ROLE_USER');
INSERT INTO USER_AUTHORITY (USER_ID, AUTHORITY_NAME) VALUES (3, 'ROLE_USER');
INSERT INTO USER_AUTHORITY (USER_ID, AUTHORITY_NAME) VALUES (4, 'ROLE_ADMIN');
```
```java
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

      if (new EmailValidator().isValid(login, null)) {
         return userRepository.findOneWithAuthoritiesByEmailIgnoreCase(login)
            .map(user -> createSpringSecurityUser(login, user))
            .orElseThrow(() -> new UsernameNotFoundException("User with email " + login + " was not found in the database"));
      }

      String lowercaseLogin = login.toLowerCase(Locale.ENGLISH);
      return userRepository.findOneWithAuthoritiesByUsername(lowercaseLogin)
         .map(user -> createSpringSecurityUser(lowercaseLogin, user))
         .orElseThrow(() -> new UsernameNotFoundException("User " + lowercaseLogin + " was not found in the database"));

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
```
```java
package org.zerhusen.security.repository;

import org.springframework.data.jpa.repository.EntityGraph;
import org.springframework.data.jpa.repository.JpaRepository;
import org.zerhusen.security.model.User;

import java.util.Optional;

public interface UserRepository extends JpaRepository<User, Long> {

   @EntityGraph(attributePaths = "authorities")
   Optional<User> findOneWithAuthoritiesByUsername(String username);

   @EntityGraph(attributePaths = "authorities")
   Optional<User> findOneWithAuthoritiesByEmailIgnoreCase(String email);

}
``` 
## response 1:
The issue seems to be that the `loadUserByUsername` method in `UserModelDetailsService` class is not handling the case where the login could be an email or a username. It only checks if the login is a valid email and if it is, it tries to find the user by email. If the login is not a valid email, it assumes it's a username and tries to find the user by username. 

However, in your case, the username itself is a valid email ('user@user.com'), so the method tries to find the user by email, which is empty in the database for this user, hence the user is not found.

To fix this, you should modify the `loadUserByUsername` method to first try to find the user by username, and if the user is not found, then try to find the user by email.

Here is the modified `loadUserByUsername` method:

```java
@Override
@Transactional
public UserDetails loadUserByUsername(final String login) {
   log.debug("Authenticating user '{}'", login);

   String lowercaseLogin = login.toLowerCase(Locale.ENGLISH);
   Optional<User> userByUsername = userRepository.findOneWithAuthoritiesByUsername(lowercaseLogin);

   if(userByUsername.isPresent()) {
      return createSpringSecurityUser(lowercaseLogin, userByUsername.get());
   } else if (new EmailValidator().isValid(login, null)) {
      return userRepository.findOneWithAuthoritiesByEmailIgnoreCase(login)
         .map(user -> createSpringSecurityUser(login, user))
         .orElseThrow(() -> new UsernameNotFoundException("User with email " + login + " was not found in the database"));
   } else {
      throw new UsernameNotFoundException("User " + lowercaseLogin + " was not found in the database");
   }
}
```

This way, the method will first try to find the user by username, and if it doesn't find it, it will try to find the user by email. If it still doesn't find the user, it will throw a `UsernameNotFoundException`.