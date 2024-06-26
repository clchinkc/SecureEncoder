FROM node:18.17.1-alpine
WORKDIR /app
COPY package.json ./
RUN rm -rf node_modules package-lock.json && npm cache clear --force && npm install
COPY . .
EXPOSE 3000
CMD ["npm", "run", "dev"]
