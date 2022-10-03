CREATE DEFINER=`root`@`localhost` PROCEDURE `crearUsuario`(IN n_email varchar(50),
IN n_contra varchar(30))
BEGIN
	if (select exists (select 1 from usuario where correo = n_email)) then
		select 'Usuario ya existe!!';
	else
        insert into usuario values (n_email, n_contra);

    end if;
END