import logging

logger = logging.getLogger(__name__)

class LicenseRouter:
    """
    A database router to control all database operations on models in the
    'licenses' app, routing OldLicense and Endo to 'old_lic_data' and License and related models to 'default'.
    """

    def db_for_read(self, model, **hints):
        logger.debug(f"db_for_read called for model: {model._meta.model_name}, app_label: {model._meta.app_label}")
        try:
            if model._meta.app_label == 'licenses':
                # Old database models
                if model._meta.model_name in ['oldlicense', 'endo']:
                    logger.debug(f"Routing {model._meta.model_name} to old_lic_data database")
                    return 'old_lic_data'
                # New database models
                elif model._meta.model_name in ['license', 'endorsenumber', 'licenseupdation', 'licensevehicle', 'updationtype', 'vehicletype']:
                    logger.debug(f"Routing {model._meta.model_name} to default database")
                    return 'default'
                else:
                    logger.debug(f"Model {model._meta.model_name} not handled by router, using default")
            else:
                logger.debug(f"Model {model._meta.model_name} not in licenses app, using default")
        except Exception as e:
            logger.error(f"Error in db_for_read for model {model._meta.model_name}: {e}")
        return None

    def db_for_write(self, model, **hints):
        logger.debug(f"db_for_write called for model: {model._meta.model_name}, app_label: {model._meta.app_label}")
        try:
            if model._meta.app_label == 'licenses':
                # Old database models
                if model._meta.model_name in ['oldlicense', 'endo']:
                    logger.debug(f"Routing {model._meta.model_name} to old_lic_data database for write")
                    return 'old_lic_data'
                # New database models
                elif model._meta.model_name in ['license', 'endorsenumber', 'licenseupdation', 'licensevehicle', 'updationtype', 'vehicletype']:
                    logger.debug(f"Routing {model._meta.model_name} to default database for write")
                    return 'default'
                else:
                    logger.debug(f"Model {model._meta.model_name} not handled by router for write, using default")
            else:
                logger.debug(f"Model {model._meta.model_name} not in licenses app for write, using default")
        except Exception as e:
            logger.error(f"Error in db_for_write for model {model._meta.model_name}: {e}")
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if both models are in the licenses app and in the same DB.
        """
        if obj1._meta.app_label == 'licenses' and obj2._meta.app_label == 'licenses':
            db_obj1 = self.db_for_read(obj1.__class__)
            db_obj2 = self.db_for_read(obj2.__class__)
            if db_obj1 and db_obj2 and db_obj1 == db_obj2:
                return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Ensure that the License and related models only appear in the 'default' DB,
        and OldLicense and Endo only in 'old_lic_data'.
        """
        if app_label == 'licenses':
            if model_name in ['oldlicense', 'endo']:
                return db == 'old_lic_data'
            elif model_name in ['license', 'endorsenumber', 'licenseupdation', 'licensevehicle', 'updationtype', 'vehicletype']:
                return db == 'default'
        return None