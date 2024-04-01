-- Функция для чтения файла .env и извлечения значений переменных
local function read_env_file(filename)
	local env_values = {}
	for line in io.lines(filename) do
		local key, value = line:match("^%s*([^#=%s]+)%s*=%s*'([^']*)'%s*$")
		if key then
			env_values[key] = value
		end
	end
	return env_values
end

-- Чтение значений из файла .env
local env_values = read_env_file(".env")

-- Создание строки подключения к PostgreSQL, если данные присутствуют в .env
local postgres_uri = nil
if
	env_values["POSTGRES_USER"]
	and env_values["POSTGRES_PASSWORD"]
	and env_values["POSTGRES_HOST"]
	and env_values["POSTGRES_PORT"]
	and env_values["POSTGRES_NAME"]
then
	postgres_uri = string.format(
		"postgres://%s:%s@%s:%s/%s",
		env_values["POSTGRES_USER"],
		env_values["POSTGRES_PASSWORD"],
		env_values["POSTGRES_HOST"],
		env_values["POSTGRES_PORT"],
		env_values["POSTGRES_NAME"]
	)
end

-- Создание строки подключения к Redis, если данные присутствуют в .env
local redis_uri = nil
if env_values["REDIS_HOST"] and env_values["REDIS_PORT"] then
	redis_uri = string.format("redis://%s:%s/0", env_values["REDIS_HOST"], env_values["REDIS_PORT"])
end

-- Проверка наличия файла db.sqlite3
local cwd = vim.fn.getcwd()
local sqlite_file = cwd .. "/db.sqlite3"
local sqlite_uri = nil
if vim.fn.filereadable(sqlite_file) == 1 then
	sqlite_uri = "sqlite://" .. sqlite_file
end

-- Формирование таблицы vim.g.dbs только с данными, если они присутствуют
local dbs = {}
if postgres_uri then
	dbs.postgres = postgres_uri
end
if redis_uri then
	dbs.redis = redis_uri
end
if sqlite_uri then
	dbs.sqlite = sqlite_uri
end

-- Присваивание сформированной таблицы vim.g.dbs
vim.g.dbs = dbs
