-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 23-12-2022 a las 22:31:11
-- Versión del servidor: 10.4.24-MariaDB
-- Versión de PHP: 8.1.6

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `chatbot`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `cliente`
--

CREATE TABLE `cliente` (
  `cliente_id` int(11) NOT NULL,
  `cliente_nombre` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `cliente_email` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `cliente_direccion` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `cliente_nombreUsuario` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `cliente_telefono` varchar(25) COLLATE utf8mb4_unicode_ci NOT NULL,
  `cliente_suscrito` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `cliente`
--

INSERT INTO `cliente` (`cliente_id`, `cliente_nombre`, `cliente_email`, `cliente_direccion`, `cliente_nombreUsuario`, `cliente_telefono`, `cliente_suscrito`) VALUES
(1, 'jose', 'jose@', 'fdsadf', 'jose', '', 0),
(5, 'starling', 'starling@gmail.com', 'calle10', 'user1', '', 0),
(6, 'starlindfasdg', 'starling@gmasdfail.com', 'calle10', 'user1', '', 0),
(7, 'jose1', 'daivelcanela@gmail.com', 'calle10', 'tatielunik', '', 1),
(8, 'starling', 'default@gmamil.com', 'lat: latitude, log: longitude', 'starlingvoxel', 'telefono', 0),
(9, 'starlin', 'tatielunik@gmail.com', '19.502075 -70.749114', 'starlingvasquez4', '8298728425', 0);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `flores`
--

CREATE TABLE `flores` (
  `flor_id` int(11) NOT NULL,
  `flor_nombre` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `flor_descripcion` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `flor_precio` int(11) NOT NULL,
  `flor_imagen` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `flores`
--

INSERT INTO `flores` (`flor_id`, `flor_nombre`, `flor_descripcion`, `flor_precio`, `flor_imagen`) VALUES
(1, 'AMOROSSA', 'Hermoso arreglo de flores. Divinas para recordar', 500, 'https://i2.wp.com/floristeriabonsai.net/wp-content/uploads/2018/02/FB-218b.jpg?fit=848%2C1280&ssl=1'),
(3, 'BOUQUET', 'Hermoso arreglo de flores. Divinas para recordar', 800, 'https://i1.wp.com/floristeriabonsai.net/wp-content/uploads/2018/02/FB-269A-RD7500.00.jpg?fit=1076%2C'),
(5, 'RBG99', 'Hermoso arreglo de flores. Divinas para recordar\r\n', 4000, 'https://i1.wp.com/floristeriabonsai.net/wp-content/uploads/2018/02/FB-269A-RD7500.00.jpg?fit=1076%2C'),
(6, 'MB60', 'Hermoso arreglo de flores. Divinas para recordar', 4500, 'https://i2.wp.com/floristeriabonsai.net/wp-content/uploads/2020/11/corona-RB73.jpg?resize=600%2C741&');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `orden`
--

CREATE TABLE `orden` (
  `orden_id` int(11) NOT NULL,
  `cliente_id` int(11) DEFAULT NULL,
  `orden_estatus` int(11) DEFAULT NULL,
  `orden_creado` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `orden`
--

INSERT INTO `orden` (`orden_id`, `cliente_id`, `orden_estatus`, `orden_creado`) VALUES
(1, 7, 3, '2022-12-14 05:16:28.511714'),
(2, 7, 3, '2022-12-14 05:21:35.558960'),
(3, 7, 2, '2022-12-14 05:32:31.954076'),
(4, 7, 2, '2022-12-14 06:19:46.537442'),
(5, 7, 2, '2022-12-14 07:22:21.079302'),
(6, 7, 2, '2022-12-14 22:30:28.349235'),
(7, 8, 2, '2022-12-17 01:33:34.719230'),
(8, 8, 2, '2022-12-19 15:45:33.839076'),
(9, 9, 2, '2022-12-22 15:25:27.357898'),
(10, 9, 2, '2022-12-22 15:46:20.210959'),
(11, 9, 2, '2022-12-22 20:58:09.517820'),
(12, 9, 2, '2022-12-22 21:41:10.051466'),
(13, 9, 2, '2022-12-22 22:52:27.965495'),
(14, 9, 2, '2022-12-22 23:14:18.350247'),
(15, 9, 2, '2022-12-22 23:15:26.115695'),
(16, 9, 2, '2022-12-22 23:44:36.334413'),
(17, 9, 2, '2022-12-23 00:20:31.278337'),
(18, 9, 4, '2022-12-23 14:48:30.965361');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `ordenitem`
--

CREATE TABLE `ordenitem` (
  `ordenItem_id` int(11) DEFAULT NULL,
  `flor_id` int(11) DEFAULT NULL,
  `cantidad` int(11) DEFAULT NULL,
  `precio` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `ordenitem`
--

INSERT INTO `ordenitem` (`ordenItem_id`, `flor_id`, `cantidad`, `precio`) VALUES
(1, 6, 1, 4500),
(2, 6, 1, 4500),
(3, 6, 1, 4500),
(4, 6, 1, 4500),
(5, 6, 1, 4500),
(6, 6, 1, 4500),
(6, 5, 1, 4000),
(7, 6, 1, 4500),
(7, 6, 1, 4500),
(8, 1, 1, 500),
(8, 6, 1, 4500),
(9, 5, 1, 4000),
(10, 6, 1, 4500),
(11, 6, 1, 4500),
(12, 3, 1, 800),
(13, 6, 1, 4500),
(14, 5, 1, 4000),
(14, 3, 1, 800),
(14, 1, 1, 500),
(14, 5, 1, 4000),
(14, 6, 1, 4500),
(15, 5, 1, 4000),
(15, 6, 1, 4500),
(16, 6, 1, 4500),
(17, 6, 1, 4500),
(17, 3, 1, 800),
(18, 3, 1, 800),
(18, 1, 1, 500);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `ordenstatustipo`
--

CREATE TABLE `ordenstatustipo` (
  `OrderStatusTypeId` tinyint(4) DEFAULT NULL,
  `Descripcion` varchar(9) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `ordenstatustipo`
--

INSERT INTO `ordenstatustipo` (`OrderStatusTypeId`, `Descripcion`) VALUES
(1, 'Pagada'),
(2, 'Pendiente'),
(3, 'Cancelada'),
(4, 'Carrito');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `cliente`
--
ALTER TABLE `cliente`
  ADD PRIMARY KEY (`cliente_id`);

--
-- Indices de la tabla `flores`
--
ALTER TABLE `flores`
  ADD PRIMARY KEY (`flor_id`);

--
-- Indices de la tabla `orden`
--
ALTER TABLE `orden`
  ADD PRIMARY KEY (`orden_id`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `cliente`
--
ALTER TABLE `cliente`
  MODIFY `cliente_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT de la tabla `flores`
--
ALTER TABLE `flores`
  MODIFY `flor_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT de la tabla `orden`
--
ALTER TABLE `orden`
  MODIFY `orden_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=19;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
