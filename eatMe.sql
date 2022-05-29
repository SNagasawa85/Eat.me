-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema eat_me_db
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `eat_me_db` ;

-- -----------------------------------------------------
-- Schema eat_me_db
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `eat_me_db` DEFAULT CHARACTER SET utf8 ;
USE `eat_me_db` ;

-- -----------------------------------------------------
-- Table `eat_me_db`.`users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `eat_me_db`.`users` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `first_name` VARCHAR(45) NULL,
  `last_name` VARCHAR(45) NULL,
  `email` VARCHAR(255) NULL,
  `pw_hash` CHAR(60) NULL,
  `created_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `eat_me_db`.`foods`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `eat_me_db`.`foods` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(255) NULL,
  `exp` DATE NULL DEFAULT NULL,
  `price` DECIMAL NULL DEFAULT NULL,
  `user_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_food_users_idx` (`user_id` ASC) VISIBLE,
  CONSTRAINT `fk_food_users`
    FOREIGN KEY (`user_id`)
    REFERENCES `eat_me_db`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `eat_me_db`.`shoplists`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `eat_me_db`.`shoplists` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `notes` TEXT NULL DEFAULT NULL,
  `users_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_shoplists_users1_idx` (`users_id` ASC) VISIBLE,
  CONSTRAINT `fk_shoplists_users1`
    FOREIGN KEY (`users_id`)
    REFERENCES `eat_me_db`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `eat_me_db`.`shoplists_has_food`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `eat_me_db`.`shoplists_has_food` (
  `shoplist_id` INT NOT NULL,
  `food_id` INT NOT NULL,
  PRIMARY KEY (`shoplist_id`, `food_id`),
  INDEX `fk_shoplists_has_food_food1_idx` (`food_id` ASC) VISIBLE,
  INDEX `fk_shoplists_has_food_shoplists1_idx` (`shoplist_id` ASC) VISIBLE,
  CONSTRAINT `fk_shoplists_has_food_shoplists1`
    FOREIGN KEY (`shoplist_id`)
    REFERENCES `eat_me_db`.`shoplists` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_shoplists_has_food_food1`
    FOREIGN KEY (`food_id`)
    REFERENCES `eat_me_db`.`foods` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
