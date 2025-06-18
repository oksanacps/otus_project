from selenium.webdriver.common.by import By


class Header:
    NAV_BAR = (By.CSS_SELECTOR, '[class="navbar navbar-default"]')
    SPRING_BUTTON = (By.CSS_SELECTOR, '.navbar-brand')
    HOME_BUTTON = (By.CSS_SELECTOR, '[routerlink="welcome"]')
    OWNERS_BUTTON = (By.XPATH, '//a[contains(text(), "Owners")]')
    SEARCH_OWNER_DROP_DOWN_BUTTON = (By.CSS_SELECTOR, '[href="/petclinic/owners"]')
    ADD_NEW_OWNER_DROP_DOWN_BUTTON = (By.CSS_SELECTOR, '[href="/petclinic/owners/add"]')
    VETERINARIANS_BUTTON = (By.CSS_SELECTOR, '[routerlink="/vets"]')
    ALL_VETS_DROP_DOWN_BUTTON = (By.CSS_SELECTOR, '[href="/petclinic/vets"]')
    ADD_NEW_VET_CLINIC_DROP_DOWN = (By.CSS_SELECTOR, '[href="/petclinic/vets/add"]')
    PET_TYPES_BUTTON = (By.CSS_SELECTOR, '[routerlink="/pettypes"]')
    SPECIALTIES_BUTTON = (By.CSS_SELECTOR, '[routerlink="/specialties"]')

