# High Level Design

This is the high level design of the Line OA.

## Architecture

![architecture](./assets/architecture.excalidraw.png)

## Schema

```mermaid
erDiagram
    users {
        int64 id PK
        string line_id "UNIQUE"
        numeric height
        numeric weight
        int age
        int8 gender
        timestamp created_at
        timestamp updated_at
    }

    histories{
        int64 id PK
        string line_id FK
        int8 meal
        string description
        bytes photo
        int64 calories_kcal "calories(kcal)"
        int64 protein_g "protein(g)"
        int64 carbs_g "carbs(g)"
        int64 fat_g "fat(g)"
        int64 sodium_mg "sodium(mg)"
        string ai_description
        string ai_suggest
        timestamp created_at
        timestamp updated_at
    }

    users ||--o{ histories: "user's records"
```

## Features

### First use

- User need to give some basic information for the Line OA at the first time.

#### Flow

```mermaid
sequenceDiagram
    participant LineOA
    participant API
    participant DB 
    LineOA->>+API: Send some message.
    API<<->>DB: Retrieve user basic information.
    alt basic information exist
        API->>API: Process something.
        API->>LineOA: Return processed result.
    else
        API->>API: Set register process to true.
        API->>LineOA: Ask for user's heigh.
        LineOA->>API: Send user's heigh.
        API->>API: Store user's heigh.
        API->>LineOA: Ask for user's weight.
        LineOA->>API: Send user's weight.
        API->>API: Store user's weight.
        API->>LineOA: Ask for user's age.
        LineOA->>API: Send user's age.
        API->>API: Store user's age.
        API->>LineOA: Ask for user's gender.
        LineOA->>API: Send user's gender.
        API->>API: Store user's gender.
        API->>LineOA: Ask user to check the information.
        LineOA->>API: Confirm the information.
        API->>DB: Store the user information.
        API->>API: Set register process to false.
        API->>-LineOA: Welcome message.
    end
```

### Meal Analysis

- User can enter the meal information and retrieve suggestion from AI.

#### Flow

```mermaid
sequenceDiagram
    participant LineOA
    participant API
    participant DB 
    participant GPT
    LineOA->>+API: Send which meal the user wants to analysis.
    API->>API: Store which meal the user wants to analysis.
    API->>LineOA: Ask user to enter the meal description.
    LineOA->>API: Send the meal description.
    API->>API: Store the meal description.
    API->>LineOA: Ask user to send the meal picture.
    LineOA->>API: Send the meal picture.
    API<<->>DB: Retrieve daily history.
    API->>API: Generate prompt.
    API<<->>GPT: Retrieve the ai analysis.
    API->>DB: Store the meal analysis.
    API->>-LineOA: Send the meal analysis.
```

### Get Daily Report

- Users can retrieve the daily meal report which analysis by AI.

#### Flow

```mermaid
sequenceDiagram
    participant LineOA
    participant API
    participant DB 
    participant GPT
    LineOA->>+API: Send get daily meal report.
    API<<->>DB: Retrieve daily history.
    API->>API: Generate prompt.
    API<<->>GPT: Retrieve the ai analysis.
    API->>-LineOA: Send the daily meal report.
```

### Get Meal Report With Specific Time Range

- Users can retrieve the meal report with specific time range which analysis by AI. The time range is from today to the previous 90 days.

#### Flow

```mermaid
sequenceDiagram
    participant LineOA
    participant API
    participant DB 
    participant GPT
    LineOA->>+API: Send get meal report with time range.
    API->>LineOA: Ask user to enter the start date.
    LineOA->>API: Send the start date.
    API->>API: Store the start date.
    API->>LineOA: Ask user to enter the end date.
    LineOA->>API: Send the end date.
    API<<->>DB: Retrieve the meal histories with time range.
    API->>API: Generate prompt.
    API<<->>GPT: Retrieve the ai analysis.
    API->>-LineOA: Send the meal report with time range.
```
