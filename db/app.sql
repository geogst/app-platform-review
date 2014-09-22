SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL';


-- -----------------------------------------------------
-- Table `platform`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `platform` ;

CREATE  TABLE IF NOT EXISTS `platform` (
  `id` INT NOT NULL AUTO_INCREMENT ,
  `name` VARCHAR(45) NOT NULL ,
  PRIMARY KEY (`id`) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `category`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `category` ;

CREATE  TABLE IF NOT EXISTS `category` (
  `id` INT NOT NULL AUTO_INCREMENT ,
  `name` VARCHAR(45) NULL ,
  PRIMARY KEY (`id`) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `app`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `app` ;

CREATE  TABLE IF NOT EXISTS `app` (
  `id` INT NOT NULL AUTO_INCREMENT ,
  `name` VARCHAR(255) NOT NULL ,
  PRIMARY KEY (`id`) )
ENGINE = InnoDB;

CREATE UNIQUE INDEX `name_UNIQUE` ON `app` (`name` ASC) ;


-- -----------------------------------------------------
-- Table `listing`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `listing` ;

CREATE  TABLE IF NOT EXISTS `listing` (
  `app` INT NOT NULL ,
  `platform` INT NOT NULL ,
  `category` INT NOT NULL ,
  `price` DECIMAL(8,2) NULL ,
  PRIMARY KEY (`app`, `platform`) ,
  CONSTRAINT `fk_listing_2a`
    FOREIGN KEY (`app` )
    REFERENCES `app` (`id` )
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_listing_1aa`
    FOREIGN KEY (`platform` )
    REFERENCES `platform` (`id` )
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_listing_1bb`
    FOREIGN KEY (`category` )
    REFERENCES `category` (`id` )
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;

CREATE INDEX `fk_listing_2` ON `listing` (`app` ASC) ;

CREATE INDEX `fk_listing_1` ON `listing` (`platform` ASC) ;

CREATE INDEX `fk_listing_1bvb` ON `listing` (`category` ASC) ;



SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
