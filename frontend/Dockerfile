# build env
FROM node:21.7.1-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . ./
RUN npm run build && mkdir -p result_build && cp -r build/* result_build/
EXPOSE 3000
CMD ["npm", "start"]
