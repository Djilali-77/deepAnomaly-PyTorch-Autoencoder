FROM node:22-alpine

WORKDIR /app

COPY package.json package-lock.json* ./
RUN npm install

COPY . .

EXPOSE 5173

# Start the Vite dev server and let the browser outside the container reach it
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]